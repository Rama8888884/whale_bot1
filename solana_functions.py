from dotenv import load_dotenv
import os
import aiohttp
import sqlite3
import logging

load_dotenv()

def is_valid_solana_address(address):
    return len(address) == 44 and all(c.isalnum() or c == '_' for c in address)

def setup_database():
    con = sqlite3.connect('whale_db.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS whales_solana 
                   (address TEXT PRIMARY KEY, nickname TEXT, txnhash TEXT)''')
    con.commit()
    con.close()

def add_wallet_to_db(address, nickname):
    con = sqlite3.connect('whale_db.db')
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO whales_solana (address, nickname, txnhash) VALUES (?, ?, 'new')", (address, nickname))
    con.commit()
    con.close()

def get_wallets_from_db():
    con = sqlite3.connect('whale_db.db')
    cur = con.cursor()
    cur.execute("SELECT address, nickname FROM whales_solana")
    wallets = cur.fetchall()
    con.close()
    return wallets

async def get_market_cap(token_address):
    url = f"https://public-api.solscan.io/token/meta?tokenAddress={token_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    market_cap = data.get("marketCap", 0)
                    return int(market_cap)
                return None
    except Exception as e:
        logging.error(f"Error fetching market cap: {e}")
        return None

async def fetch_transactions(wallet_address):
    url = f"https://public-api.solscan.io/account/transactions?address={wallet_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json() if response.status == 200 else None
    except Exception as e:
        logging.error(f"Error fetching transactions: {e}")
        return None

async def filter_transactions(wallet, nickname, context):
    transactions = await fetch_transactions(wallet)
    if transactions:
        for tx in transactions:
            try:
                token_address = tx.get("parsedInstruction", {}).get("info", {}).get("mint", "")
                market_cap = await get_market_cap(token_address)

                if market_cap and market_cap < int(os.getenv("MARKET_CAP_THRESHOLD", 1000000)):
                    tx_type = tx.get("parsedInstruction", {}).get("type", "")
                    amount = tx.get("parsedInstruction", {}).get("info", {}).get("amount", 0)

                    message = (f"🚨 Whale Alert 🚨\n"
                               f"Nickname: {nickname}\n"
                               f"Wallet: {wallet}\n"
                               f"Action: Accumulating\n"
                               f"Token: {token_address}\n"
                               f"Amount: {int(amount) / (10**9)} SOL\n"
                               f"Market Cap: ${market_cap}")
                    await context.bot.send_message(chat_id=context.job.chat_id, text=message)
            except Exception as e:
                logging.error(f"Error processing transaction: {e}")
