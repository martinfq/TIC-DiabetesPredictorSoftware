from neo4j import GraphDatabase


class Config:
    NEO4J_URI = "neo4j+s://0bd4f8f9.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "FcnDEyWSyY9oo5Y15LWAJd2H172KDeOv4NF5TlVAeAM"


class Database:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()


db = Database()
