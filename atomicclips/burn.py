"""
Subtitle burning utilities for AtomicClips Phase 0.

Uses ffmpeg CLI to burn a .srt file into the input video producing an output video.
Requires ffmpeg to be installed on the system PATH.
"""
import os
import shlex
import subprocess
import logging

logger = logging.getLogger(__name__)


def check_ffmpeg():
    """Check ffmpeg is available on PATH. Raises RuntimeError if not found."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        raise RuntimeError('ffmpeg not found on PATH. Please install ffmpeg and ensure it is on your PATH.')
    except subprocess.CalledProcessError:
        # ffmpeg exists but returned an error; we'll accept its existence.
        return True
    return True


def burn_subtitles(input_video: str, srt_path: str, output_video: str, font_size: int = 24) -> None:
    """Burn subtitles (SRT) into a video using ffmpeg.

    Args:
        input_video: path to input video
        srt_path: path to .srt file
        output_video: path for output video
        font_size: fontsize for ASS style (applies when using force_style)
    """
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")
    if not os.path.exists(srt_path):
        raise FileNotFoundError(f"SRT file not found: {srt_path}")

    # Ensure ffmpeg exists
    check_ffmpeg()

    # Build subtitles filter. Use subtitles filter with force_style to control size.
    # We must escape the srt path for ffmpeg filter. Use shlex.quote for shell safety;
    # when passing args as list to subprocess, quoting isn't necessary, but filter parsing
    # requires single quotes around the path on some platforms. We'll wrap the path.
    srt_escaped = srt_path.replace("'", "\\'")
    filter_arg = f"subtitles='{srt_escaped}':force_style='Fontsize={font_size}'"

    cmd = [
        'ffmpeg', '-y', '-i', input_video,
        '-vf', filter_arg,
        '-c:a', 'copy',
        output_video
    ]

    logger.info('Running ffmpeg command: %s', ' '.join(shlex.quote(p) for p in cmd))

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        logger.error('ffmpeg failed: %s', e.stderr.decode('utf-8', errors='ignore'))
        raise

    logger.info('ffmpeg finished successfully')
