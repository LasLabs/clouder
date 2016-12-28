FROM clouder/base:3.4
MAINTAINER Dave Lasley <dave@laslabs.com>

RUN addgroup -S redoctober \
    && adduser -S -g redoctober redoctober

# Install Build Dependencies

ENV buildDeps "build-base \
               gcc \
               git \
               go \
               libtool \
               openssl \
               runit@community"

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --no-cache $buildDeps

# Install Red October
RUN git clone --depth=1 https://github.com/cloudflare/redoctober.git /usr/lib/go/src/github.com/cloudflare/redoctober
RUN go install github.com/cloudflare/redoctober

# Setup Environment
ENV RO_DATA=/var/lib/redoctober/data \
    RO_CERTS=$RO_DATA/server.crt \
    RO_KEYS=$RO_DATA/server.pem

ENTRYPOINT ["/go/src/github.com/cloudflare/redoctober/scripts/docker-entrypoint.sh"]

CMD ["redoctober", \
    "-addr=:8080", \
    "-vaultpath=$RO_DATA/diskrecord.json", \
    "-certs=$RO_CERTS", \
    "-keys=$RO_KEYS"]
