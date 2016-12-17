FROM clouder/base:3.4
MAINTAINER Dave Lasley <dave@laslabs.com>

RUN apk add --no-cache openssl \
                       openssl-dev \
                       pip

RUN pip install cryptography

# Enter
ENTRYPOINT ["openssl"]
CMD ["cat"]
