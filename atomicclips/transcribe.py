"""
Transcription utilities for AtomicClips Phase 0.

Uses OpenAI Whisper (python package 'whisper') to transcribe an input video and
writes an intermediate .srt subtitle file with timestamps.

The implementation keeps things simple and CPU-friendly by default so it can
run in Google Colab or on a phone-controlled cloud environment.
"""
import os
import math
import whisper
import logging


logger = logging.getLogger(__name__)


def _format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp: HH:MM:SS,mmm"""
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    hours = ms // 3_600_000
    ms = ms % 3_600_000
    minutes = ms // 60_000
    ms = ms % 60_000
    secs = ms // 1000
    ms = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def transcribe_to_srt(input_path: str, srt_path: str, model_name: str = 'small', language: str = None, device: str = 'cpu') -> None:
    """Transcribe input media to SRT using Whisper.

    Args:
        input_path: path to input video/audio file
        srt_path: path to write .srt file
        model_name: whisper model name (tiny, base, small, medium, large)
        language: optional language code (eg 'en') or None to auto-detect
        device: torch device string (cpu or cuda)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    logger.info('Loading Whisper model "%s" (device=%s)', model_name, device)
    try:
        model = whisper.load_model(model_name, device=device)
    except Exception as e:
        logger.exception('Failed to load Whisper model: %s', e)
        raise

    # Run transcription. We request timestamps/segments so we can create SRT entries.
    logger.info('Running transcription. This may take a while...')
    try:
        # `transcribe` returns a dict with 'segments' when `verbose` is False.
        result = model.transcribe(input_path, language=language)
    except Exception as e:
        logger.exception('Whisper transcription failed: %s', e)
        raise

    segments = result.get('segments') or []

    if not segments:
        logger.warning('No segments returned by Whisper')

    # Write SRT
    logger.info('Writing %d subtitle segments to %s', len(segments), srt_path)
    with open(srt_path, 'w', encoding='utf-8') as fh:
        for i, seg in enumerate(segments, start=1):
            start = seg.get('start', 0.0)
            end = seg.get('end', start + seg.get('duration', 0.0))
            text = seg.get('text', '').strip()
            # Whisper often includes leading spaces/newlines
            if not text:
                continue
            fh.write(f"{i}\n")
            fh.write(f"{_format_timestamp(start)} --> {_format_timestamp(end)}\n")
            # Escape any SRT-unfriendly chars if needed (keep simple)
            fh.write(text + "\n\n")

    logger.info('SRT written successfully')
