FROM node:22.23.3-bookworm-slim AS css

WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY tailwind.config.js ./
COPY PACEr/templates/ PACEr/templates/
COPY PACEr/static/ PACEr/static/
RUN npm run build:css

FROM python:3.12.15-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_URL=sqlite:////data/pacer.db \
    TMPDIR=/data/tmp \
    HOME=/data

WORKDIR /app/PACEr
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt gunicorn

RUN groupadd --gid 10001 pacer \
    && useradd --uid 10001 --gid pacer --home-dir /data --no-create-home pacer \
    && mkdir -p /data/tmp \
    && chown -R pacer:pacer /data

COPY PACEr/ /app/PACEr/
COPY docker/gunicorn.conf.py /app/gunicorn.conf.py
COPY --from=css /build/PACEr/static/build/theme.css /app/PACEr/static/build/theme.css

# No credentials are needed at build time. Coolify can supply SOURCE_COMMIT
# as a build argument; a runtime ASSET_VERSION can override this value.
ARG SOURCE_COMMIT=local
ARG ASSET_VERSION=${SOURCE_COMMIT}
ENV ASSET_VERSION=${ASSET_VERSION}

USER pacer
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3).close()"]

CMD ["gunicorn", "--config", "/app/gunicorn.conf.py", "app:create_app()"]
