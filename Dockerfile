FROM python:3.11-slim
LABEL maintainer="Mariano Ruiz <mrsarm@gmail.com>"

ENV CXXFLAGS="-mtune=intel -Os -pipe" \
    PROCESS_TYPE="web" \
    PORT=8000 \
    NUM_WORKERS=3 \
    NUM_THREADS=3 \
    REQUEST_TIMEOUT=20

WORKDIR /usr/src/app

COPY requirements/requirements-dev.txt \
     requirements/requirements-test.txt \
     requirements/requirements-prod.txt \
         /usr/src/app/

RUN buildDeps=' \
        build-essential \
        libuv1-dev \
        libpq-dev \
        libevent-dev \
        libpcre3-dev \
        zlib1g-dev \
        libbz2-dev \
        libxml2-dev \
    ' \
    && apt-get update -y \
    && apt-get install -y \
        $buildDeps \
        postgresql-client \
        libpq5 \
        libuv1 \
        libpcre3 \
        zlib1g \
        libbz2-1.0 \
        libxml2 \
        gettext \
    # adding "worker" user
    && useradd -ms /bin/bash worker \
    && chown -R worker:worker /usr/src/app \
    && mkdir /usr/tmp \
    && chown worker:worker /usr/tmp \
    && chown worker:worker requirements*.txt \
    && pip install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir \
        honcho \
    && pip3 install --no-cache-dir -r requirements-test.txt \
    && pip3 install --no-cache-dir -r requirements-dev.txt \
    && pip3 install --no-cache-dir -r requirements-prod.txt \
    # cleanup
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY --chown=worker ./ ./

ARG BUILD
LABEL build=${BUILD}
RUN echo "Build: $BUILD" > image_build \
    && echo "UTC: $(date --utc +%FT%R)" >> image_build

# In a "prod" image, the migrations process should be executed
# before the image and kept on git or whatever VCS
RUN honcho start collectstatic compilemessages \
    && honcho start --no-prefix makemigrations \
    && rm *.sqlite3 *.log \
    && chown worker -R *

USER worker

CMD ["sh", "-c", "exec honcho start --no-prefix $PROCESS_TYPE"]
