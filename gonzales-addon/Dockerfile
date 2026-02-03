# ===== Builder: compile Python packages =====
ARG BUILD_FROM
FROM ${BUILD_FROM} AS builder

# BUILD_VERSION invalidates cache when addon version changes
ARG BUILD_VERSION

# Install build dependencies for Python packages (uvloop, httptools, etc.)
RUN apk add --no-cache \
    git \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Cache buster: rebuild gonzales package when addon version bumps
RUN echo "Building gonzales backend for addon v${BUILD_VERSION}" && \
    pip3 install --no-cache-dir --target=/opt/gonzales \
    "gonzales @ git+https://github.com/akustikrausch/gonzales.git#subdirectory=backend"

# Clone custom_components for HA integration (will be copied to /config on startup)
RUN git clone --depth 1 https://github.com/akustikrausch/gonzales-ha.git /tmp/gonzales-ha && \
    mkdir -p /opt/gonzales-integration && \
    cp -r /tmp/gonzales-ha/custom_components/gonzales /opt/gonzales-integration/ && \
    rm -rf /tmp/gonzales-ha

# ===== Runtime: lean image =====
FROM ${BUILD_FROM}

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Gonzales" \
    org.opencontainers.image.authors="akustikrausch" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/akustikrausch/gonzales-ha" \
    org.opencontainers.image.source="https://github.com/akustikrausch/gonzales-ha" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"

RUN apk add --no-cache bash curl ca-certificates jemalloc

COPY --from=builder /opt/gonzales /opt/gonzales
COPY --from=builder /opt/gonzales-integration /opt/gonzales-integration

RUN ARCH=$(uname -m) && \
    case "$ARCH" in aarch64) A=aarch64;; x86_64) A=x86_64;; *) echo "Unsupported arch: $ARCH" && exit 1;; esac && \
    curl -fsSL "https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-${A}.tgz" \
      | tar xz -C /usr/local/bin speedtest && \
    chmod +x /usr/local/bin/speedtest

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8099/api/v1/status > /dev/null || exit 1

ENV PYTHONPATH=/opt/gonzales
ENV LD_PRELOAD=/usr/lib/libjemalloc.so.2

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
