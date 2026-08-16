import os

from dotenv import load_dotenv

load_dotenv()


COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")
COGNODB_DATABASE = os.getenv("COGNODB_DATABASE", "neo4j")


if not COGNODB_URI:
    raise RuntimeError("COGNODB_URI is not set")

if not COGNODB_USERNAME:
    raise RuntimeError("COGNODB_USERNAME is not set")

if not COGNODB_PASSWORD:
    raise RuntimeError("COGNODB_PASSWORD is not set")