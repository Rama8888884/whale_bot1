# Base image using Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Create a directory for the application
WORKDIR /app

# Copy only the requirements file first to leverage Docker's caching
COPY requirements.txt /app/

# Update and install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential

# Upgrade pip and install basic tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Try installing minimal Telegram requirements first
RUN pip install --no-cache-dir python-telegram-bot==22.1 python-dotenv==1.1.0

# Copy the entire project into the working directory
COPY . /app

# Expose the port your application will run on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
