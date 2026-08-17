import os
import subprocess
from atomicclips.burn import burn_subtitles
from unittest import mock

def test_burn_subtitles_cmd(monkeypatch, tmp_path):
    # create fake input video and srt with spaces and single quotes to simulate a tricky path
    in_video = tmp_path / "in video.mp4"
    in_video.write_bytes(b"\x00")
    srt_path = tmp_path / "weird 'name'.srt"
    srt_path.write_text("1\n00:00:00,000 --> 00:00:01,000\nHello\n", encoding="utf-8")
    out_video = tmp_path / "out.mp4"

    captured = {}

    def fake_run(cmd, stdout, stderr, check):
        # Save the command for inspection and simulate success
        captured["cmd"] = cmd
        class R: pass
        return R()

    monkeypatch.setattr("subprocess.run", fake_run)
    # Also monkeypatch check_ffmpeg to not require real ffmpeg for this unit test
    monkeypatch.setattr("atomicclips.burn.check_ffmpeg", lambda: True)

    burn_subtitles(str(in_video), str(srt_path), str(out_video))

    assert "ffmpeg" in captured["cmd"][0]
    # there should be '-vf' and the following item should contain 'subtitles='
    assert "-vf" in captured["cmd"]
    vf_index = captured["cmd"].index("-vf")
    assert "subtitles=" in captured["cmd"][vf_index + 1]
    # output filename should be last arg
    assert str(out_video) in captured["cmd"]
