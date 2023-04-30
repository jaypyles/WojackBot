IMAGE_NAME=docker-wojack
CONTAINER_NAME= wojackbot

# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run Docker container
run:
	docker run -d --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Clean up Docker image and container
# Stops Docker container if running
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
