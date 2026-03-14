import os
import io
import torch
import numpy as np
import librosa
import soundfile as sf
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
from pydantic import BaseModel
from typing import List

from encoder import inference as encoder
from encoder.params_model import model_embedding_size as speaker_embedding_size
from synthesizer.inference import Synthesizer
from vocoder import inference as vocoder
from utils.default_models import ensure_default_models

import tempfile

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Real-Time Voice Cloning API")

# Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

# Global models
synthesizer = None

@app.on_event("startup")
async def load_models():
    global synthesizer
    print("Preparing the encoder, the synthesizer and the vocoder...")
    models_dir = Path("saved_models")
    ensure_default_models(models_dir)
    
    # Load models
    encoder.load_model(models_dir / "default" / "encoder.pt")
    synthesizer = Synthesizer(models_dir / "default" / "synthesizer.pt")
    vocoder.load_model(models_dir / "default" / "vocoder.pt")
    print("Models loaded successfully.")

class SynthesizeRequest(BaseModel):
    text: str
    embedding: List[float]

@app.post("/embed")
async def get_embedding(file: UploadFile = File(...)):
    """
    接收一個語音文件，返回說話者的嵌入向量 (Embedding)。
    """
    try:
        # 使用臨時文件
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        try:
            # 使用 librosa 讀取音訊
            wav, sampling_rate = librosa.load(tmp_path, sr=None)
            
            # 預處理
            preprocessed_wav = encoder.preprocess_wav(wav, sampling_rate)
            
            # 提取嵌入
            embed = encoder.embed_utterance(preprocessed_wav)
            
            return {"embedding": embed.tolist()}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize")
async def synthesize(request: SynthesizeRequest):
    """
    使用提供的嵌入向量和文本生成語音。
    """
    global synthesizer
    try:
        embed = np.array(request.embedding)
        
        # 生成 mel 頻譜
        texts = [request.text]
        embeds = [embed]
        specs = synthesizer.synthesize_spectrograms(texts, embeds)
        spec = specs[0]
        
        # 生成波形
        generated_wav = vocoder.infer_waveform(spec)
        
        # 後處理
        generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
        generated_wav = encoder.preprocess_wav(generated_wav)
        
        # 寫入 Buffer 並返回
        buffer = io.BytesIO()
        sf.write(buffer, generated_wav.astype(np.float32), synthesizer.sample_rate, format='WAV')
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clone")
async def clone_voice(text: str = Form(...), file: UploadFile = File(...)):
    """
    一鍵克隆：接收語音文件和文本，直接返回生成的語音。
    """
    global synthesizer
    try:
        # 使用臨時文件
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        try:
            # 1. 提取嵌入
            wav, sampling_rate = librosa.load(tmp_path, sr=None)
            preprocessed_wav = encoder.preprocess_wav(wav, sampling_rate)
            embed = encoder.embed_utterance(preprocessed_wav)
            
            # 2. 生成語音
            texts = [text]
            embeds = [embed]
            specs = synthesizer.synthesize_spectrograms(texts, embeds)
            spec = specs[0]
            generated_wav = vocoder.infer_waveform(spec)
            
            # 3. 後處理
            generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
            generated_wav = encoder.preprocess_wav(generated_wav)
            
            # 寫入 Buffer 並返回
            buffer = io.BytesIO()
            sf.write(buffer, generated_wav.astype(np.float32), synthesizer.sample_rate, format='WAV')
            buffer.seek(0)
            
            return StreamingResponse(buffer, media_type="audio/wav")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
