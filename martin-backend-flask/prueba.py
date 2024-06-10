from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
NEO4J_URI = "neo4j+s://0bd4f8f9.databases.neo4j.io"
NEO4J_AUTH = ("neo4j","FcnDEyWSyY9oo5Y15LWAJd2H172KDeOv4NF5TlVAeAM")


with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
    driver.verify_connectivity()
