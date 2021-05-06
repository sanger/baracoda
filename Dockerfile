# Use slim for a smaller image size and install only the required packages
FROM python:3.8-slim

# Needed for something...
ENV PYTHONUNBUFFERED 1

# libpq-dev & gcc: required by psycopg2
RUN apt-get update && apt-get install -y \
  curl \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install the package manager - pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Change the working directory for all proceeding operations
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#workdir
WORKDIR /code

# "items (files, directories) that do not require ADD’s tar auto-extraction capability, you should always use COPY."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy
COPY Pipfile .
COPY Pipfile.lock .

# Install both default and dev packages so that we can run the tests against this image
RUN pipenv install --dev --ignore-pipfile --system --deploy

# Copy all the source to the image
COPY . .

# "The best use for ENTRYPOINT is to set the image’s main command, allowing that image to be run as though it was that
#   command (and then use CMD as the default flags)."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#entrypoint
# have a look in .flaskenv for configured run options
ENTRYPOINT ["flask"]
CMD ["run"]

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -Lf http://localhost:8000/health || exit 1
