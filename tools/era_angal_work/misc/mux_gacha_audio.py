import sys
import wave
from pathlib import Path

import av
import numpy as np
from PIL import Image


def read_wav(path):
    with wave.open(str(path), "rb") as source:
        channels = source.getnchannels()
        rate = source.getframerate()
        width = source.getsampwidth()
        frames = source.readframes(source.getnframes())
    if width != 2 or rate != 44100:
        raise RuntimeError(f"expected 44.1kHz 16-bit WAV: {path} ({rate}Hz, {width * 8}bit)")
    data = np.frombuffer(frames, dtype=np.int16).reshape(-1, channels)
    if channels == 1:
        data = np.repeat(data, 2, axis=1)
    return data.astype(np.float32)


def add_track(mix, track, start_seconds, gain):
    start = int(start_seconds * 44100)
    if start >= len(mix):
        return
    end = min(len(mix), start + len(track))
    mix[start:end] += track[: end - start] * gain


input_video = Path(sys.argv[1])
audio_dir = Path(sys.argv[2])
output_mp4 = Path(sys.argv[3])
output_wav = Path(sys.argv[4])
sequence_mode = "--sequence" in sys.argv[5:]
rarity = "sr"
voice_path = None
for index, option in enumerate(sys.argv[5:-1], start=5):
    if option == "--rarity":
        rarity = sys.argv[index + 1].lower()
    if option == "--voice":
        voice_path = Path(sys.argv[index + 1])
card_sound = audio_dir / f"gacha_card_{rarity}.wav"

input_container = av.open(str(input_video))
frames = [frame.to_image().convert("RGB") for frame in input_container.decode(video=0)]
input_container.close()

duration = len(frames) / 30.0
mix = np.zeros((int(duration * 44100) + 44100, 2), dtype=np.float32)
add_track(mix, read_wav(audio_dir / "gacha_theme.wav"), 0.0, 0.28)
if sequence_mode:
    # The sequence is 2.0s desk/touch, 1.33s dark transition, then the
    # 2.23s SR reveal.  Put the extracted game sounds at those visual beats.
    add_track(mix, read_wav(audio_dir / "gacha_touch.wav"), 0.82, 0.70)
    add_track(mix, read_wav(audio_dir / "gacha_petal.wav"), 2.05, 0.60)
    add_track(mix, read_wav(audio_dir / "gacha_turn_over.wav"), 3.18, 0.78)
    add_track(mix, read_wav(card_sound), 3.33, 0.85)
else:
    add_track(mix, read_wav(card_sound), 0.0, 0.85)
    add_track(mix, read_wav(audio_dir / "gacha_petal.wav"), 0.30, 0.60)
    add_track(mix, read_wav(audio_dir / "gacha_turn_over.wav"), 0.88, 0.78)
if voice_path is not None:
    # The card line plays after the reveal has settled.
    add_track(mix, read_wav(voice_path), 5.15 if sequence_mode else 1.15, 0.95)
mix = np.clip(mix[: int(duration * 44100)], -32768, 32767).astype(np.int16)

output_wav.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(output_wav), "wb") as target:
    target.setnchannels(2)
    target.setsampwidth(2)
    target.setframerate(44100)
    target.writeframes(mix.tobytes())

output_mp4.parent.mkdir(parents=True, exist_ok=True)
container = av.open(str(output_mp4), "w", format="mp4")
video = container.add_stream("libx264", rate=30)
video.options = {"crf": "16", "preset": "slow"}
video.width = 1272
video.height = 708
video.pix_fmt = "yuv420p"
audio = container.add_stream("aac", rate=44100)
audio.layout = "stereo"
audio.bit_rate = 192000

for index, image in enumerate(frames):
    if image.size != (1272, 708):
        image = image.resize((1272, 708), Image.Resampling.LANCZOS)
    frame = av.VideoFrame.from_ndarray(np.asarray(image), format="rgb24")
    frame.pts = index
    for packet in video.encode(frame):
        container.mux(packet)
for offset in range(0, len(mix), 1024):
    chunk = mix[offset : offset + 1024]
    if len(chunk) == 0:
        continue
    frame = av.AudioFrame.from_ndarray(np.ascontiguousarray(chunk.T), format="s16p", layout="stereo")
    frame.sample_rate = 44100
    frame.pts = offset
    for packet in audio.encode(frame):
        container.mux(packet)
for packet in video.encode():
    container.mux(packet)
for packet in audio.encode():
    container.mux(packet)
container.close()

print(output_mp4)
print(output_wav)
