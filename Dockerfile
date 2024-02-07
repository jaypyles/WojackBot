# Use Python slim as the base image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

# Update pip and install required packages
RUN pip install --upgrade pip && pip install pdm

# Set the working directory to /app
WORKDIR /app

# Copy the bot project files to the container
COPY . .

# Install bot dependencies
RUN pdm install

# Expose the bot port
EXPOSE 3000

# Start the bot
CMD ["pdm", "run", "bot"]
