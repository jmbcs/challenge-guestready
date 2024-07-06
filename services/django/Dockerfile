# Use the official slim Python image as the base image
FROM python:3.11.6-slim-bullseye


# Set the working directory in the container
WORKDIR /djangoserver

# Copy the current directory contents into the container at /djangoserver
COPY . .

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose port 8000 (adjust if your Django application runs on a different port)
EXPOSE 8000

# Run migrations, then start the Django development server
CMD ["sh", "-c", "python3 django_project/manage.py migrate && python3 django_project/manage.py runserver 0.0.0.0:8000"]
