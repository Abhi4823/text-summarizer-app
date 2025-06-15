# Use official Python base image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy all your code into the container
COPY . .

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
