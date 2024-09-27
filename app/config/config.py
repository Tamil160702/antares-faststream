class Config:

  class EventStatus:
    start="Starting"
    completed="Completed"
    error="Error"

  class Postgres:
    database = "postgres"
    user = "postgres"
    password = "Pr0j$!rius2024"  # Redact before using
    host = "35.200.244.209"
    port = "5432"
    
  class Scylla:
    host = "34.93.251.52" 
    port = 9042
    keyspace = "alpha_dev"

  class Neo4j:
    host = "neo4j://35.200.226.248:7687"     #old_host
    # host = "neo4j://35.200.136.177"        #new_host
    user = "neo4j"
    password = "neo4j123"

  class Nats:
    server = "nats://35.200.211.19:4222"     #old_server
    #  server = "nats://34.47.138.110:4222"  #new_server

  
  class Druid:
    server = "http://34.100.179.171:8888"    #old_server
    # server = "http://34.47.143.241:8888"   #new_server

    
