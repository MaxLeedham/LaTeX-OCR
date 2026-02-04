FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu
WORKDIR /latexocr
ADD pix2tex /latexocr/pix2tex/
ADD setup.py /latexocr/
ADD README.md /latexocr/
RUN pip install -e .[api]
RUN python -m pix2tex.model.checkpoints.get_latest_checkpoint

ENTRYPOINT ["uvicorn", "pix2tex.api.app:app", "--host", "0.0.0.0", "--port", "8502"]
