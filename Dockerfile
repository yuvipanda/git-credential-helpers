FROM alpine:3.16

RUN apk add --no-cache py3-pip py3-wheel

WORKDIR /srv
ADD . .
RUN python3 setup.py bdist_wheel

FROM alpine:3.16

RUN apk add --no-cache py3-pip git

COPY --from=0 /srv/dist/*.whl /tmp
RUN pip install --no-cache /tmp/*.whl
