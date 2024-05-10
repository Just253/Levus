import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as _:
    r.adjust_for_ambient_noise(_)

while True:
  with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)

  # recognize speech using Google Speech Recognition
  try:
      text = r.recognize_google(audio, language='es-PE')
      print("You said: " + text)
  except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
