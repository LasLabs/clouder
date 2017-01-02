FROM clouder/base:3.4
MAINTAINER Dave Lasley <dave@laslabs.com>

ARG RO_CERTPASSWD="password"
ARG RO_COMMONNAME="localhost"

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
RUN git clone --depth=1 https://github.com/cloudflare/redoctober.git /usr/lib/go/src/github.com/cloudflare/redoctober \
    && go install github.com/cloudflare/redoctober

ENV GOROOT="/usr/lib/go" \
    GOPATH="/gopath" \
    GOBIN="/gopath/bin" \
    PATH="$PATH:$GOROOT/bin:$GOPATH/bin"

# Path isn't persisting for some reason.
RUN ln -s "$GOROOT/bin/redoctober" /usr/bin

# Setup Environment
ENV RO_DATA="/var/lib/redoctober/data"
ENV RO_CERTS="${RO_DATA}/server.crt" \
    RO_KEYS="${RO_DATA}/server.pem" \
    RO_CERTPASSWD="${RO_CERTPASSWD}" \
    RO_COMMONNAME="${RO_COMMONNAME}"

ENTRYPOINT ["/usr/lib/go/src/github.com/cloudflare/redoctober/scripts/docker-entrypoint.sh"]

CMD ["redoctober", \
     "-addr=:8080", \
     "-vaultpath=/var/lib/redoctober/data/diskrecord.json", \
     "-certs=/var/lib/redoctober/data/server.crt", \
     "-keys=/var/lib/redoctober/data/server.pem"]
