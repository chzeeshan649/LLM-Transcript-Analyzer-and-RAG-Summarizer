# Use Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching layer)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
