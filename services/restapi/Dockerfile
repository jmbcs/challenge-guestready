# Command to run the application# Use the official slim Python image as the base image
FROM python:3.11.6-slim-bullseye

# Set the working directory
WORKDIR /restapi

# Copy the project files into the container
COPY . .

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -e .

CMD ["sh", "-c", "alembic upgrade head && python3 api"]
