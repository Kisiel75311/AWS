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

ENV AWS_DEFAULT_REGION='us-east-1'
ENV AWS_COGNITO_USER_POOL_ID='us-east-1_azAQV5aWO'
ENV AWS_COGNITO_USER_POOL_CLIENT_ID='25qht9jpfc2d7cmngemroac4s4'
ENV AWS_COGNITO_USER_POOL_CLIENT_SECRET='1fvtp624s3hvbhblbifou0o8idjm379jbg0fn8qlg0jaoto303jj'


# Run tests and generate Allure reports
RUN pytest --alluredir=/app/reports || true

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# The command to run when the container starts
CMD ["/app/entrypoint.sh"]
