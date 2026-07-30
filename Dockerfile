FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory '*'

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

WORKDIR /repo
ENTRYPOINT ["premerge"]
CMD ["--help"]
