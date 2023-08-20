

def validate(id: str, jsonfile: dict):
    if(jsonfile['id'] == id):
        return True
    
    return False