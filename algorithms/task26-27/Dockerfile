# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY ./ ./
WORKDIR /app/ITbaza/
EXPOSE 8000
CMD LS
CMD python3 ./manage.py runserver 0.0.0.0:8000