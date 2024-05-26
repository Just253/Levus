import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

model = Model(model_name="vosk-model-small-es-0.42")
samplerate = 16000

with sd.RawInputStream(samplerate=samplerate, blocksize=16000, dtype="int16", channels=1, callback=callback):
    print("Listening... Press Ctrl+C to stop.")
    rec = KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            print(rec.Result())
