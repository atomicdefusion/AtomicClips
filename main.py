#!/usr/bin/env python3
"""AtomicClips Phase 0 - minimal video -> whisper -> srt -> burned subtitles pipeline

Usage:
  python main.py --input input.mp4 --output output.mp4 [--model small]

This script coordinates transcription and subtitle burning. See atomicclips/transcribe.py
and atomicclips/burn.py for the implementation.
"""
import argparse
import sys
import os
import logging
from atomicclips.transcribe import transcribe_to_srt
from atomicclips.burn import burn_subtitles, check_ffmpeg


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def parse_args():
    p = argparse.ArgumentParser(description='AtomicClips Phase 0 - generate burned subtitles from a video')
    p.add_argument('--input', '-i', required=True, help='Input video file path')
    p.add_argument('--output', '-o', required=True, help='Output video file path')
    p.add_argument('--model', '-m', default='small', help='Whisper model name (tiny, base, small, medium, large)')
    p.add_argument('--language', '-l', default=None, help='Language for Whisper (eg: en). If omitted, Whisper will auto-detect')
    p.add_argument('--srt', default=None, help='Path to write intermediate .srt file (defaults to <output>.srt)')
    p.add_argument('--device', default='cpu', help='Torch device to use (cpu or cuda). Default: cpu')
    return p.parse_args()


def main():
    args = parse_args()

    input_path = args.input
    output_path = args.output
    model_name = args.model
    language = args.language
    device = args.device
    srt_path = args.srt or os.path.splitext(output_path)[0] + '.srt'

    # Basic checks
    if not os.path.exists(input_path):
        logging.error('Input file does not exist: %s', input_path)
        sys.exit(2)

    try:
        check_ffmpeg()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(3)

    try:
        logging.info('Transcribing %s with Whisper model=%s (device=%s)...', input_path, model_name, device)
        transcribe_to_srt(input_path, srt_path, model_name=model_name, language=language, device=device)
        logging.info('Wrote subtitles to %s', srt_path)
    except Exception as e:
        logging.exception('Transcription failed: %s', e)
        sys.exit(4)

    try:
        logging.info('Burning subtitles into video...')
        burn_subtitles(input_path, srt_path, output_path)
        logging.info('Output written to %s', output_path)
    except Exception as e:
        logging.exception('Failed to burn subtitles: %s', e)
        sys.exit(5)


if __name__ == '__main__':
    main()
