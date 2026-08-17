```markdown
@@
- On Colab you can run:
-    !apt update && apt install -y ffmpeg
-    !pip install -q -U whisper torch
+ On Colab you can run:
+    !apt update && apt install -y ffmpeg
+    !pip install -q -U openai-whisper torch
@@
-    --model small      Whisper model to use (tiny, base, small, medium, large)
-    --language en      Hint the language to Whisper
-    --srt /path/out.srt  Path to write intermediate .srt (default: same as output with .srt)
+    --model small      Whisper model to use (tiny, base, small, medium, large)
+    --language en      Hint the language to Whisper
+    --srt /path/out.srt  Path to write intermediate .srt (default: same as output with .srt)
+    --device cpu       Torch device to use (cpu or cuda). Default: cpu
```
