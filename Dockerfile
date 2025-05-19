# Use a stable Python version
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Try installing with a different approach - one by one for essential packages
RUN pip install --upgrade pip setuptools wheel && \
    echo "Installing essential packages separately..." && \
    pip install python-telegram-bot==22.1 && \
    pip install python-dotenv==1.1.0 && \
    echo "Essential packages installed successfully"

# Copy your application code
COPY . .

# Expose port if needed
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
