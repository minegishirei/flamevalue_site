FROM nginx:latest

USER root

ENV LETSENCRYPT_HOSTS short-tips.info
#【ドメイン名 スペース区切りで複数指定可】

ENV LETSENCRYPT_MAIL minegishirei@gmail.com
#【窓口メールアドレス】

ENV LETSENCRYPT_SUBJECT "/C=JP/ST=Tokyo/L=Shinagawa/CN=r3"
#←仮証明書用の記載内容】

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
      openssl \
      certbot \
    && rm -rf /var/lib/apt/lists/*

COPY .well-known/acme-challenge /.well-known/acme-challenge/



COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD /start.sh


