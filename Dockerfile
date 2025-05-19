# Base image using Python 3.9
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
    apt-get install -y --no-install-recommends gcc build-essential && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Copy the entire project into the working directory
COPY . /app
# Expose the port your application will run on
EXPOSE 8000
# Run the application
CMD ["python", "main.py"]
