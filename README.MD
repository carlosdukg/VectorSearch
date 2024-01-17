# MongoDB Vector Search

Vector search on multiple document vector indexes for custom change specifications.

## Installation

Use Docker to installed and run the application.

```bash
https://www.docker.com/products/docker-desktop/
```

## Usage

```bash
git clone https://github.com/carlosdukg/VectorSearch.git

# Build and run the image locally
docker build --tag {YOUR-TAG-NAME} .

docker run --detach --publish 3100:3100 {YOUR-TAG-NAME}

# Use Vector APIs
http://localhost:3100/docs
```