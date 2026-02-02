ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache bash curl ca-certificates git

# Ookla speedtest CLI (static binary, arch-dependent)
RUN ARCH=$(uname -m) && \
    case "$ARCH" in aarch64) A=aarch64;; x86_64) A=x86_64;; esac && \
    curl -fsSL \
      "https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-${A}.tgz" \
      | tar xz -C /usr/local/bin speedtest

# Gonzales backend from main repo
RUN pip3 install --no-cache-dir \
    "gonzales @ git+https://github.com/akustikrausch/gonzales.git#subdirectory=backend"

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
