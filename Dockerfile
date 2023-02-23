FROM python:3.10.5-slim-buster

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing upload codecov
        curl \
        # deps for building python deps
        build-essential \
        # cleaning cache
        && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# copy only requirements, to cache them in docker layer
COPY ./requirements-dev.txt /app/requirements-dev.txt

# install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /app/requirements-dev.txt

# copy docker scripts
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x '/docker-entrypoint.sh'

CMD ["/docker-entrypoint.sh"]
