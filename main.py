# import logging
import time
import pyaudio
import whisper
import numpy as np
import webrtcvad
from collections import deque

# logger = Logger('main')
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
    is_triggered = False
    frames = []
    start = time.time()
    # logging.info('starting...')
    print('starting...')
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        is_speech = vad.is_speech(data, RATE)
        if not is_triggered:
            ring_buffer.append((data, is_speech))
            n_voiced = len([f for f, _is_speech in ring_buffer if _is_speech])
            if n_voiced > .9 * ring_buffer.maxlen:
                # talking 
                is_triggered = True
                frames.extend([f for f, _ in ring_buffer])
                ring_buffer.clear()
        else:
            frames.append(data)
            ring_buffer.append((data, is_speech))
            n_unvoiced = len([f for f, _is_speech in ring_buffer if not _is_speech])
            if n_unvoiced > 0.9 * ring_buffer.maxlen:
                # stopped talking
                is_triggered = False
                audio = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
                result = model.transcribe(audio, fp16=False)["text"]
                # mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio), n_mels=model.dims.n_mels).to(model.device)
                # result = whisper.decode(model, mel, options).text
                if result.strip():
                    print(f"{result}")
                frames = []
                ring_buffer.clear()
            if time.time() - start > 5:
                start = time.time()
