FROM mysql:8.0-debian

RUN apt-get update \
    && apt-get install --no-install-recommends -y tzdata \
    && apt-get clean

ADD ./conf.d/ /etc/mysql/conf.d/

RUN chmod 644 /etc/mysql/conf.d/my.cnf