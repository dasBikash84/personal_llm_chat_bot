# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file, .env file, and app code to the working directory
COPY requirements.txt .
COPY .env .
COPY app.py .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "app.py"]