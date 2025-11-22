import os

def mime_type_validation(filename: str) -> bool:

    allowed_extension = {".zip", ".xls", ".csv"}

    _, ext = os.path.splitext(filename.lower())

    return ext in allowed_extension
    