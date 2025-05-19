# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering and to use UTF-8 encoding
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies globally (no virtual environment)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the necessary port (if needed)
EXPOSE 8000

# Run the bot
CMD ["python", "main.py"]