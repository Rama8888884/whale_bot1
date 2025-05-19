# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv

# Install the dependencies inside the virtual environment
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables to use the venv
ENV PATH="/opt/venv/bin:$PATH"

# Run the bot
CMD ["python", "main.py"]