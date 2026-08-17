import os
from atomicclips.transcribe import transcribe_to_srt

class DummyModel:
    def transcribe(self, input_path, language=None):
        # return two small segments to validate SRT formatting
        return {
            "segments": [
                {"start": 0.0, "end": 1.5, "text": " Hello world "},
                {"start": 1.6, "end": 3.0, "text": "Next line"}
            ]
        }

def test_transcribe_writes_srt(monkeypatch, tmp_path):
    # create a fake input file
    in_video = tmp_path / "in.mp4"
    in_video.write_bytes(b"\x00")
    out_srt = tmp_path / "out.srt"

    def fake_load(model_name, device=None):
        return DummyModel()

    # monkeypatch the whisper.load_model used by our module
    monkeypatch.setattr("atomicclips.transcribe.whisper.load_model", fake_load)

    transcribe_to_srt(str(in_video), str(out_srt), model_name="tiny", language="en", device="cpu")

    content = out_srt.read_text(encoding="utf-8")
    assert "00:00:00,000 --> 00:00:01,500" in content
    assert "Hello world" in content
    assert "00:00:01,600 --> 00:00:03,000" in content
