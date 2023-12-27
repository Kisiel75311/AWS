# Use the official Python image as the base image
FROM python:3.9.13

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code to the container
COPY . .

# Set environment variables
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV FLASK_ENV=development


# Run tests
RUN pytest --alluredir=/app/reports

# The command to run when the container starts
CMD ["flask", "run", "--debug"]
