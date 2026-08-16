from neo4j import GraphDatabase

from app.config import (
    COGNODB_URI,
    COGNODB_USERNAME,
    COGNODB_PASSWORD,
)

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME,COGNODB_PASSWORD)
)
def verify_database_connection():
    driver.verify_connectivity()

def get_driver():
    return driver