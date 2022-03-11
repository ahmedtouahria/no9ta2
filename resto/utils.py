import uuid
def generate_random_code():
    code=str(uuid.uuid4()).replace('-','')[:10].upper()
    return code