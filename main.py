import time
import pyaudio
import whisper
import numpy as np
import webrtcvad
from collections import deque

options = whisper.DecodingOptions(language="English")
vad = webrtcvad.Vad(2)
model = whisper.load_model("small")

RATE = 16000
# CHUNK = 2048
CHUNK_DURATION_MS = 30
CHUNK = int(RATE * CHUNK_DURATION_MS / 1000)
PADDING_DURATION_MS = 300
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)


p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK
)


if __name__ == "__main__":
    ring_buffer = deque(maxlen=NUM_PADDING_CHUNKS)
    frames = []
    start = time.time()
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(np.frombuffer(data, np.int16).astype(np.float32) / 32768.0)
        # todo: adaptive, record for as long as someone is talking
        if time.time() - start > 5:
            audio = np.concatenate(frames)
            result = model.transcribe(audio, fp16=False)["text"]
            # mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio), n_mels=model.dims.n_mels).to(model.device)
            # result = whisper.decode(model, mel, options).text
            if result.strip():
                print(f"{result}")
            frames = []
            start = time.time()
