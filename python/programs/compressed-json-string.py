import json
import zlib
import base64

with open('/home/niklas/F/ice-cases/test-suite/cfd_test_history.json', 'r') as f:
    data = json.load(f)
original_text = json.dumps(data) # "This is a very long string " * 50

# --- COMPRESSION ---

# 1. Compress the string to bytes
compressed_data = zlib.compress(original_text.encode('utf-8'))

# 2. Encode to Base64 (still bytes)
base64_bytes = base64.b64encode(compressed_data)

# 3. Decode to a UTF-8 string for JSON
json_ready_string = base64_bytes.decode('utf-8')

# Store in JSON
json_output = json.dumps({"payload": json_ready_string})

print(f"Original size: {len(original_text)} chars")
print(f"JSON payload size: {len(json_ready_string)} chars")
# Output example: Original size: 1350 chars -> JSON payload size: 60 chars

# --- DECOMPRESSION ---

# 1. Load from JSON
data_loaded = json.loads(json_output)

# 2. Convert string back to Base64 bytes
decoded_b64 = base64.b64decode(data_loaded["payload"])

# 3. Decompress back to original string
restored_text = zlib.decompress(decoded_b64).decode('utf-8')

assert original_text == restored_text
print("Successfully restored!")

