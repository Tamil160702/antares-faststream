#!/bin/bash

if [ $# -ne 1 ]; then
    
    
    echo "Usage: $0 <subject>"
    
    
    
    exit 1
fi



subject="$1"

docker run --rm -it --net=host natsio/nats-box nats sub "$subject"



