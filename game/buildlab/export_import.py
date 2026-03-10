from game.utils.serialization import encode_build, decode_build

def export_build(build: dict) -> str:
    return encode_build(build)

def import_build(code: str) -> dict:
    return decode_build(code)
