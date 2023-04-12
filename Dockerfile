# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir /app/dataset

# Copy the rest of the application code into the container
COPY . .

# Expose port 80 for the application
EXPOSE 80

# Set the environment variable for the application
ENV ENVIRONMENT=production

# Run the command to start the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
