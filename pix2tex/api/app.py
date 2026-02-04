# Adapted from https://github.com/kingyiusuen/image-to-latex/blob/main/api/app.py

from http import HTTPStatus
from fastapi import FastAPI, File, UploadFile, Form, Response
from PIL import Image
from io import BytesIO
from pix2tex.cli import LatexOCR
from fastapi.middleware.cors import CORSMiddleware

model = None
app = FastAPI(title='pix2tex API', redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


@app.on_event('startup')
async def load_model():
    global model
    if model is None:
        model = LatexOCR()


@app.get('/')
def root():
    '''Health check.'''
    response = {
        'message': HTTPStatus.OK.phrase,
        'status-code': HTTPStatus.OK,
        'data': {},
    }
    return response


@app.post('/predict/')
async def predict(file: UploadFile = File(...)) -> str:
    """Predict the Latex code from an image file.

    Args:
        file (UploadFile, optional): Image to predict. Defaults to File(...).

    Returns:
        str: Latex prediction
    """
    global model
    image = Image.open(file.file)
    return model(image)

@app.options("/predict")
@app.options("/predict/")
async def options_predict():
    return Response(status_code=200)

@app.post('/bytes/')
async def predict_from_bytes(file: bytes = File(...)) -> str:  # , size: str = Form(...)
    """Predict the Latex code from a byte array

    Args:
        file (bytes, optional): Image as byte array. Defaults to File(...).

    Returns:
        str: Latex prediction
    """
    global model
    #size = tuple(int(a) for a in size.split(','))
    image = Image.open(BytesIO(file))
    return model(image, resize=False)
