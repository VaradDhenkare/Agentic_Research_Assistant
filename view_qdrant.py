
from qdrant_client import QdrantClient

# Path to your existing Qdrant storage
db_path = r"db_qdrant"

client = QdrantClient(path=db_path)

# Display all collections
collections = client.get_collections().collections

print("Collections:")
for collection in collections:
    print("-", collection.name)

# Read records from the collection
collection_name = "agentic_research"

records, next_offset = client.scroll(
    collection_name=collection_name,
    limit=10,
    with_payload=True,
    with_vectors=False
)

print("\nStored documents:")

for record in records:
    print("\nID:", record.id)
    print("Payload:", record.payload)

client.close()
