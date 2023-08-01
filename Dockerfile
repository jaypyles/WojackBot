# Use Python slim as the base image
FROM python:slim

# Update pip and install required packages
RUN pip install --upgrade pip && pip install pdm

# Set the working directory to /app
WORKDIR /app

# Copy the bot project files to the container
COPY . .

# Install bot dependencies
RUN pdm sync

# Expose the bot port
EXPOSE 3000

# Start the bot
CMD ["pdm", "run", "bot"]
