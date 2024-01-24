FROM python:3.8.3-buster

# Set the working directory
WORKDIR /app

# Copy the source code
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Sett the working directory to the handlers folder
WORKDIR /app/handlers

# Run the HTTP server defined in request_handler.py
CMD ["python", "request_handler.py"]
