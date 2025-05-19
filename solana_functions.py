from dotenv import load_dotenv
import os
import aiohttp
import sqlite3
import logging

load_dotenv()

def is_valid_solana_address(address: str) -> bool:
    # Solana addresses are base58, no underscores allowed, length 44
    if len(address) != 44:
        return False
    allowed_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in allowed_chars for c in address)

def setup_database():
    con = sqlite3.connect('whale_db.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS whales_solana 
                   (address TEXT PRIMARY KEY, nickname TEXT, txnhash TEXT)''')
    con.commit()
    con.close()

def add_wallet_to_db(address: str, nickname: str):
    con = sqlite3.connect('whale_db.db')
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO whales_solana (address, nickname, txnhash) VALUES (?, ?, 'new')",
                (address, nickname))
    con.commit()
    con.close()

def get_wallets_from_db():
    con = sqlite3.connect('whale_db.db')
    cur = con.cursor()
    cur.execute("SELECT address, nickname FROM whales_solana")
    wallets = cur.fetchall()
    con.close()
    return wallets

async def get_market_cap(token_address: str):
    url = f"https://public-api.solscan.io/token/meta?tokenAddress={token_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    market_cap = data.get("marketCap", 0)
                    return int(market_cap) if market_cap else 0
                logging.warning(f"Failed to fetch market cap, status: {response.status}")
                return 0
    except Exception as e:
        logging.error(f"Error fetching market cap: {e}")
        return 0

async def fetch_transactions(wallet_address: str):
    url = f"https://public-api.solscan.io/account/transactions?address={wallet_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                logging.warning(f"Failed to fetch transactions for {wallet_address}, status: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error fetching transactions: {e}")
        return None

async def filter_transactions(wallet: str, nickname: str, context):
    transactions = await fetch_transactions(wallet)
    if not transactions:
        logging.info(f"No transactions found for wallet {wallet}")
        return

    for tx in transactions:
        try:
            parsed_instr = tx.get("parsedInstruction", {})
            info = parsed_instr.get("info", {})
            token_address = info.get("mint", "")
            market_cap = await get_market_cap(token_address)
            threshold = int(os.getenv("MARKET_CAP_THRESHOLD", "1000000"))

            if market_cap and market_cap < threshold:
                tx_type = parsed_instr.get("type", "")
                amount = info.get("amount", 0)

                message = (
                    f"🚨 Whale Alert 🚨\n"
                    f"Nickname: {nickname}\n"
                    f"Wallet: {wallet}\n"
                    f"Action: {tx_type or 'Accumulating'}\n"
                    f"Token: {token_address}\n"
                    f"Amount: {int(amount) / (10**9)} SOL\n"
                    f"Market Cap: ${market_cap}"
                )
                await context.bot.send_message(chat_id=context.job.chat_id, text=message)
        except Exception as e:
            logging.error(f"Error processing transaction for wallet {wallet}: {e}")