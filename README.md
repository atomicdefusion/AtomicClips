# AtomicClips — Phase 0

This repository contains Phase 0 of the AtomicClips project: a minimal proof-of-concept
video-processing pipeline that takes an input video, transcribes speech using OpenAI Whisper,
writes an intermediate .srt subtitle file, and burns those subtitles into the output video
using FFmpeg.

What Phase 0 does
- Accepts a video file
- Runs Whisper transcription to obtain timestamped segments
- Writes an intermediate .srt file for inspection
- Uses FFmpeg to burn the .srt into the video producing a subtitled output

Project structure
- main.py            CLI entrypoint for the Phase 0 pipeline
- atomicclips/
  - transcribe.py    Whisper transcription -> .srt
  - burn.py          FFmpeg subtitle burning
  - __init__.py
- requirements.txt
- .gitignore

Requirements
- Python 3.8+ (works on Colab)
- ffmpeg installed and available on PATH
- pip packages (see requirements.txt): whisper, torch

FFmpeg installation
- Ubuntu / Debian / Colab: sudo apt update && sudo apt install -y ffmpeg
- macOS (Homebrew): brew install ffmpeg
- Windows: download from https://ffmpeg.org/ and add to PATH

Whisper setup
- Install Python deps: pip install -r requirements.txt
  On Colab you can run:
    !apt update && apt install -y ffmpeg
    !pip install -q -U whisper torch

Notes: Installing torch on Colab should pull a CUDA-capable wheel if GPU runtime is used.
If you're on CPU-only, pip will install the CPU wheel.

Usage
1. From the repository root, run:

    python main.py --input /path/to/input.mp4 --output /path/to/output_subtitled.mp4

2. Optional flags:
    --model small      Whisper model to use (tiny, base, small, medium, large)
    --language en      Hint the language to Whisper
    --srt /path/out.srt  Path to write intermediate .srt (default: same as output with .srt)

Output
- The script writes an intermediate .srt file (beside the output by default) and the
  subtitled output video at the path you specify with --output.

Common errors and fixes
- ffmpeg not found: install ffmpeg and ensure it is on PATH.
- Whisper model loading too slow / out of memory: use a smaller model (tiny/base/small) or
  run on a machine with more memory. For quick tests use `--model tiny`.
- Transcription fails on weird file types: try converting to a standard mp4 or wav first.

Notes for Colab / phone-driven development
- This Phase 0 implementation intentionally uses a simple CPU-friendly default and creates
  an intermediate .srt so you can inspect the transcription before burning subtitles.
- No paid APIs or secrets are required.

Next steps (Phase 1 will add these — NOT implemented here): automatic highlight detection,
AI scoring, 9:16 cropping, animated captions, web frontend/backend, and storage integration.

