FROM clouder/base:3.4
MAINTAINER Dave Lasley <dave@laslabs.com>


RUN groupadd -r redoctober --gid=999 && useradd -r -g redoctober --uid=999 redoctober

# Install Build Dependencies

ENV buildDeps "build-base \
               gcc \
               git \
               go \
               libtool \
               openssl \
               runit"

RUN apk add --no-cache $buildDeps

# Install Red October

RUN git clone --depth=1 https://github.com/cloudflare/redoctober.git /go/src/github.com/cloudflare/redoctober

RUN go install github.com/cloudflare/redoctober

EXPOSE 8080 8081
ENV RO_CERTS=/var/lib/redoctober/data/server.crt \
    RO_KEYS=/var/lib/redoctober/data/server.pem \
    RO_DATA=/var/lib/redoctober/data \
    RO_CERTPASSWD=password \
    RO_COMMONNAME=localhost

ENTRYPOINT ["/go/src/github.com/cloudflare/redoctober/scripts/docker-entrypoint.sh"]
CMD ["redoctober", \
    "-addr=:8080", \
    "-vaultpath=/var/lib/redoctober/data/diskrecord.json", \
    "-certs=/var/lib/redoctober/data/server.crt", \
    "-keys=/var/lib/redoctober/data/server.pem"]
