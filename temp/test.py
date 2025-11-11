import time
import pyaudio
import whisper
import numpy as np

options = whisper.DecodingOptions(language='English')
model = whisper.load_model('small')

RATE = 16000
CHUNK = 2048

p = pyaudio.PyAudio()
stream = p.open(
  format=pyaudio.paInt16,
  channels=1,
  rate=RATE,
  input=True,
  frames_per_buffer=CHUNK
)

if __name__ == "__main__":
  frames = []
  start = time.time()
  print("starting...")
  while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(np.frombuffer(data, np.int16).astype(np.float32) / 32768.0)
    if time.time() - start > 5:
      audio = np.concatenate(frames)
      result = model.transcribe(audio, fp16=False)['text']
      # mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio), n_mels=model.dims.n_mels).to(model.device)
      # result = whisper.decode(model, mel, options).text
      if result.strip():
        print(f'{result}')
      frames = []
      start = time.time()
      
