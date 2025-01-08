#!/bin/bash

DELAY=10

mongosh <<EOF
var config = {
  "_id": "dbrs",
  "version": 1,
  "members": [
    { "_id": 1, "host": "haru-stock-mongo-master:27017", "priority": 2 },
    { "_id": 2, "host": "haru-stock-mongo-replica1:27017", "priority": 1 },
    { "_id": 3, "host": "haru-stock-mongo-replica2:27017", "priority": 1 }
  ]
};
rs.initiate(config, { force: true });
EOF

echo "****** Waiting for ${DELAY} seconds for replicaset configuration to be applied ******"

# sleep $DELAY
# for i in {1..10}
# do
#   echo "============================================"
#   echo "============================================"
#   echo "============================================"
#   echo "============================================"
#   mongosh --eval "rs.status()"
#   sleep 1
# done

# mongosh < /scripts/init.js
