# Initialise the Kafka cluster
# docker-compose up -d   
docker-compose -f docker-compose-expose.yml up

# Cluster 1 = Dublin
# Cluster 2 = Galway
# Cluster 3 = Cork
docker-compose scale kafka=3
