# Pull official base image
FROM ubuntu:18.04

# Set work directory
WORKDIR /home/flask-restx-boilerplate

# Install python 3.7.7
RUN apt-get update
RUN apt-get install -y python3.7 python3-pip vim
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN update-alternatives --set python /usr/bin/python3.7
RUN python -m pip install --upgrade pip

# Install dependencies
COPY ./requirements.txt /home/flask-restx-boilerplate/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Copy project directory
COPY ./app /home/flask-restx-boilerplate/app

# Copy scripts directory
COPY ./scripts/start_server.sh /home/flask-restx-boilerplate/scripts/start_server.sh
COPY ./scripts/health_check.sh /home/flask-restx-boilerplate/scripts/health_check.sh

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "sh", "/home/flask-restx-boilerplate/scripts/health_check.sh" ]

# Set environment variables
ENV FLASK_BOILERPLATE_DIR /home/flask-restx-boilerplate

# Expose the flask port
EXPOSE 5000

# Run server
CMD ["sh", "/home/flask-restx-boilerplate/scripts/start_server.sh"]
