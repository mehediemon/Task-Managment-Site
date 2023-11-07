# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TaskManagmentSite.settings

# Create and set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . /app

RUN apt-get update \
    && apt-get install -y python3.8-dev \
    libpq-dev

# Install pip requirements
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files

COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entry point to the script
ENTRYPOINT ["/app/entrypoint.sh"]


