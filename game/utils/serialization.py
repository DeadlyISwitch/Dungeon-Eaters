import base64, json, zlib

def encode_build(payload: dict) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(zlib.compress(raw)).decode()

def decode_build(code: str) -> dict:
    return json.loads(zlib.decompress(base64.urlsafe_b64decode(code.encode())).decode())
