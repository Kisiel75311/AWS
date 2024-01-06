#!/bin/bash
# entrypoint.sh

# Run database migrations
flask db upgrade

# Start the Flask application
exec flask run --debug
