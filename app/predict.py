from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .core.security import decode_token
from .core.tflite_runner import predict

router = APIRouter(prefix="/predict", tags=["Predicción"])
bearer = HTTPBearer()

def check_jwt(cred: HTTPAuthorizationCredentials = Depends(bearer)):
    user = decode_token(cred.credentials)
    if not user:
        raise HTTPException(401, "Token inválido")
    return user

@router.post("/")
async def predict_route(image: UploadFile = File(...), user: str = Depends(check_jwt)):
    if image.content_type.split("/")[0] != "image":
        raise HTTPException(400, "Se requiere un archivo de imagen")
    bytes_img = await image.read()
    return predict(bytes_img)
