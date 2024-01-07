# Use the official Python image as the base image
FROM python:3.9.13

# Update the CA trust store
RUN update-ca-certificates

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download and install allurectl
RUN wget https://github.com/allure-framework/allurectl/releases/latest/download/allurectl_linux_amd64 -O ./allurectl \
    && chmod +x ./allurectl \
    && mv ./allurectl /usr/local/bin/allurectl

# Copy the rest of your application's code to the container
COPY . .

# Set environment variables for Flask
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV FLASK_ENV=development
ENV FLASK_APP=app:build_app

# Run tests and generate Allure reports
#RUN pytest --alluredir=/app/reports

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# The command to run when the container starts
CMD ["/app/entrypoint.sh"]
