from minio import Minio
import time
from datetime import datetime
import json
import random
from io import BytesIO

client = Minio(
    "minio1:9000",
    access_key="bigdata",
    secret_key="bigdata123",
    secure=False
)

bucket = "04-streaming"
if not client.bucket_exists(bucket):
    client.make_bucket(bucket)

with open("book.txt", "r") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue

    # JSON bericht maken
    message = {
        "data": line,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Bytes maken
    data = json.dumps(message).encode("utf-8")
    object_name = f"input/line_{idx}.json"

    # Upload naar MinIO
    client.put_object(
        bucket,
        object_name,
        data=BytesIO(data),
        length=len(data),
        content_type="application/json"
    )

    print(f"Verstuurd: {object_name} -> {message}")

    # Random delay tussen 100 en 1000 ms
    time.sleep(random.uniform(0.1, 1.0))
