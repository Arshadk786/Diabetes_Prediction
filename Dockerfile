# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /api

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the svc.pkl file into the container
COPY svc.pkl .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application using uvicorn
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
