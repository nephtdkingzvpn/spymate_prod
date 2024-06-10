FROM btcpayserver/btcpayserver:1.9.0

# Install PostgreSQL client libraries
RUN apt-get update && apt-get install -y postgresql-client

# Set environment variables
ENV BTCPAYGEN_CRYPTO1=BTC
ENV BTCPAYGEN_LIGHTNING=BTC
ENV BTCPAYGEN_REVERSEPROXY=nginx

# Define volumes
VOLUME /var/lib/docker/volumes/btcpayserver_bitcoin_datadir/_data
VOLUME /root/.btcpayserver
VOLUME /etc/letsencrypt

