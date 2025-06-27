# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=kjeknfknkl23j4knkfnkr2ojfknfkjo4jrnk@
ENV SQLALCHEMY_DATABASE_URI=sqlite:///bookmarks.db

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port (optional, for local testing)
EXPOSE 5000

# Command to run app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.runner:application"]
