import os
from fastapi import UploadFile

def save_file(uploaded_file: UploadFile, upload_dir: str) -> str:
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())
    return file_path

