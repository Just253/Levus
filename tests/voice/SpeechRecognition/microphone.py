import speech_recognition as sr
import openai
from io import BytesIO

r = sr.Recognizer()
with sr.Microphone() as _:
    r.adjust_for_ambient_noise(_)

while True:
  with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)

  # recognize speech using whisper
  try:
      
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = "SpeechRecognition_audio.wav"
    client = openai.OpenAI(api_key="...")
    transcript = client.audio.transcriptions.create(file=wav_data, model="whisper-1")
    print(transcript.text)
  except sr.UnknownValueError:
      print("Whisper could not understand audio")
  except sr.RequestError as e:
      print(f"Could not request results from Whisper; {e}")
