# Base image
FROM python:3.10.5-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y netcat

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV MONGO_URI="mongodb://mongo:27017/bank"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Wait for the MongoDB service to be available
#CMD bash -c 'while ! nc -z mongo 27017; do sleep 1; done; flask run --host=0.0.0.0'

CMD ["python","bankapp.py"]
