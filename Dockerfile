# Base image
FROM python:3-alpine

# Information
LABEL maintainer="FrozenFOXX <frozenfoxx@cultoffoxx.net>"

# Variables
WORKDIR /app
ENV APPDIR="/app" \
  APP_DEPS="ffmpeg imagemagick" \
  BUILD_DEPS="build-base libffi-dev python3-dev" \
  CONFIG="/etc/beatbot/conf/beatbot.yml"

# Install package dependencies
RUN apk -U add ${APP_DEPS} ${BUILD_DEPS}

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Clean up 
RUN apk del ${BUILD_DEPS}

# Launch
ENTRYPOINT [ "./scripts/entrypoint.sh" ]
