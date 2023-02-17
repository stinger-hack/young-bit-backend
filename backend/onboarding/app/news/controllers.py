from fastapi import APIRouter, WebSocket, UploadFile, File
from onboarding.config import settings
from onboarding.storage.s3 import S3Service
from onboarding.protocol import Response

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.receive_json({"data": f"received {data}"})


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    client: S3Service = await S3Service.get_s3_client()
    contents = await file.read()
    await client.put_object(Bucket=settings.BUCKET_NAME, Key=file.filename, Body=contents)
    return Response(message=f"file {file.filename} sucessfully upload")
