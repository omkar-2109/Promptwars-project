# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port (Cloud Run sets PORT env var)
ENV PORT 8080
EXPOSE 8080

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
