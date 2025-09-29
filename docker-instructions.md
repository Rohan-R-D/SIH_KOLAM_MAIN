# Docker Instructions for Kolam Generator

## Development Dockerfile

### Why it's safe for containerization
- Uses official Python image as base for reliability
- Simple setup with minimal layers for easy debugging
- Runs as root only in development context where security is less critical

### Build Command
```
docker build -t kolam-dev -f Dockerfile.dev .
```

### Run Command
```
docker run -p 5000:5000 kolam-dev
```

## Production Dockerfile

### Why it's safe for containerization
- Creates and uses a non-root user for improved security
- Sets PYTHONUNBUFFERED=1 for proper logging in containerized environment
- Uses gunicorn for production-grade serving with multiple workers

### Build Command
```
docker build -t kolam-prod .
```

### Run Command
```
docker run -p 5000:5000 kolam-prod
```

## Additional Docker Commands

### View running containers
```
docker ps
```

### Stop a running container
```
docker stop <container_id>
```

### View logs
```
docker logs <container_id>
```

### Interactive shell in container
```
docker exec -it <container_id> /bin/bash
```