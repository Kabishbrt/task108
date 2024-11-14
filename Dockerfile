# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the app using uvicorn with reload enabled
CMD ["uvicorn", "fetch_X:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
