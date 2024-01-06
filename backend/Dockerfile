# Use the official Python image as the base image
FROM python:3.9.13

## Copy the CA certificate
#COPY cert2.crt /usr/local/share/ca-certificates/cert2.crt
#COPY cert3.crl /usr/local/share/ca-certificates/cert3.crl
#COPY certyfikat.crt /usr/local/share/ca-certificates/certyfikat.crt


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
RUN pytest --alluredir=/app/reports || true

## Upload the test results to Allure TestOps (set these as runtime environment variables)
#ENV ALLURE_ENDPOINT=https://allure-testops.sos.pus.corp
#ENV ALLURE_TOKEN=bfdb0b73-969a-4b83-a23c-4f7c35b6a5fb
#ENV ALLURE_PROJECT_ID=2
#ENV ALLURE_LAUNCH_NAME="Flask Backend Tests"
#ENV ALLURE_LAUNCH_TAGS="docker"

#RUN allurectl upload --endpoint https://allure-testops.sos.pus.corp \
#    --token bfdb0b73-969a-4b83-a23c-4f7c35b6a5fb \
#    --project-id 2 \
#    --launch-name "Flask Backend Tests" \
#    /reports

# The command to run when the container starts
CMD ["flask", "run", "--debug"]
