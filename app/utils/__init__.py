

import os
import re
import uuid

from fastapi import HTTPException, UploadFile


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

async def save_image(file: UploadFile,  UPLOAD_DIR: str) -> str:
    file_extension = sanitize_filename(os.path.splitext(file.filename)[1]) 
    file_name = f'{uuid.uuid4().hex}{file_extension}' 
    file_name_dir = os.path.join(UPLOAD_DIR, file_name)
    try:
        with open(file_name_dir, "wb") as buffer:
            # Leer y escribir el archivo de manera asíncrona
            buffer.write(await file.read())  # Leer el archivo en binario y escribirlo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    return file_name