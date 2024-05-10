import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as _:
    r.adjust_for_ambient_noise(_)

while True:
  with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)

  # recognize speech using whisper
  try:
      print("Whisper thinks you said " + r.recognize_vosk(audio, language="es")) 
      # Whisper thinks you said Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.
  except sr.UnknownValueError:
      print("Whisper could not understand audio")
  except sr.RequestError as e:
      print(f"Could not request results from Whisper; {e}")
