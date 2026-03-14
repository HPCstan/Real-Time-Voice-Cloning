# Real-Time Voice Cloning

> [!NOTE]
> **本專案已擴展！** 現在支援基於 FastAPI 的 **REST API** 與現代化的 **React Web 操作介面**。

This repository is an implementation of [Transfer Learning from Speaker Verification to
Multispeaker Text-To-Speech Synthesis](https://arxiv.org/pdf/1806.04558.pdf) (SV2TTS) with a vocoder that works in real-time. This was my [master's thesis](https://matheo.uliege.be/handle/2268.2/6801).

SV2TTS is a deep learning framework in three stages. In the first stage, one creates a digital representation of a voice from a few seconds of audio. In the second and third stages, this representation is used as reference to generate speech given arbitrary text.

**Video demonstration** (click the picture):

[![Toolbox demo](https://i.imgur.com/8lFUlgz.png)](https://www.youtube.com/watch?v=-O_hYhToKoA)

### Papers implemented

| URL                                                    | Designation            | Title                                                                                    | Implementation source                                   |
| ------------------------------------------------------ | ---------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [**1806.04558**](https://arxiv.org/pdf/1806.04558.pdf) | **SV2TTS**             | **Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis** | This repo                                               |
| [1802.08435](https://arxiv.org/pdf/1802.08435.pdf)     | WaveRNN (vocoder)      | Efficient Neural Audio Synthesis                                                         | [fatchord/WaveRNN](https://github.com/fatchord/WaveRNN) |
| [1703.10135](https://arxiv.org/pdf/1703.10135.pdf)     | Tacotron (synthesizer) | Tacotron: Towards End-to-End Speech Synthesis                                            | [fatchord/WaveRNN](https://github.com/fatchord/WaveRNN) |
| [1710.10467](https://arxiv.org/pdf/1710.10467.pdf)     | GE2E (encoder)         | Generalized End-To-End Loss for Speaker Verification                                     | This repo                                               |

## Heads up

Like everything else in Deep Learning, this repo has quickly gotten old. Many SaaS apps (often paying) will give you a better audio quality than this repository will. If you wish for an open-source solution with a high voice quality:

- Check out [paperswithcode](https://paperswithcode.com/task/speech-synthesis/) for other repositories and recent research in the field of speech synthesis.
- Check out [Chatterbox](https://github.com/resemble-ai/chatterbox) for a similar project up to date with the 2025 SOTA in voice cloning

## 🚀 Real-Time Voice Cloning API & Web UI

我們新增了一個現代化的 API 與網頁操作介面，讓您可以更方便地使用語音克隆功能，並輕鬆整合至您的機器人或應用程式中。

### 🌟 特色
- **現代化介面**: 採用玻璃擬態 (Glassmorphism) 設計。
- **簡單易用**: 支援拖放上傳音訊、直接輸入文字進行克隆。
- **高效能**: 基於 FastAPI 實作，支援多種音訊格式 (WAV, MP3, etc.)。

### 🛠️ 如何啟動 (Quick Start)

1. **環境準備**: 確保已安裝 `uv` ( astral.sh/uv )。
2. **安裝依賴與運行**:
   ```bash
   # 在專案目錄下
   uv sync --extra cpu
   uv run python fast_api.py
   ```
3. **訪問介面**:
   - **網頁操作介面**: [http://localhost:8000](http://localhost:8000)
   - **API 文件**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 📁 檔案結構說明
- `fast_api.py`: FastAPI 端點與模型載入核心邏輯。
- `static/index.html`: 基於 React 實作的單頁 Web UI。
- `test_api.py`: 提供給開發者的 API 調用測試範例。

---

## Running the toolbox (Original)

Both Windows and Linux are supported.
1. Install [ffmpeg](https://ffmpeg.org/download.html#get-packages). This is necessary for reading audio files. Check if it's installed by running in a command line
```
ffmpeg
```
2. Install uv for python package management
```
# On Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# On Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternatively, on any platform if you have pip installed you can do
pip install -U uv
```
3. Run one of the following commands
```
# Run the toolbox if you have an NVIDIA GPU
uv run --extra cuda demo_toolbox.py
# Use this if you don't
uv run --extra cpu demo_toolbox.py

# Run in command line if you don't want the GUI
uv run --extra cuda demo_cli.py
uv run --extra cpu demo_cli.py
```
Uv will automatically create a .venv directory for you with an appropriate python environment. [Open an issue](https://github.com/CorentinJ/Real-Time-Voice-Cloning/issues) if this fails for you

### (Optional) Download Pretrained Models

Pretrained models are now downloaded automatically. If this doesn't work for you, you can manually download them from [Hugging Face](https://huggingface.co/CorentinJ/SV2TTS/tree/main).

### (Optional) Download Datasets

For playing with the toolbox alone, I only recommend downloading [`LibriSpeech/train-clean-100`](https://www.openslr.org/resources/12/train-clean-100.tar.gz). Extract the contents as `<datasets_root>/LibriSpeech/train-clean-100` where `<datasets_root>` is a directory of your choosing. Other datasets are supported in the toolbox, see [here](https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Training#datasets). You're free not to download any dataset, but then you will need your own data as audio files or you will have to record it with the toolbox.
