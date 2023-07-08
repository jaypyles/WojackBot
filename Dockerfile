# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Update the package list and install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3.9 python3-pip && \
    pip3 install pdm

RUN apt-get update && apt-get install -y libjpeg-dev
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
