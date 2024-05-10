## DESCARTADO
- Desventajas
  - Requiere muchos pasos de instalacion guia  https://github.com/openai/whisper/discussions/1463 
  - Al ser complicado de instalar para el usuario rompe con el principio de Levus ser simple de instalar
  - Se logro probar tanto con nucleos CUDA y CPU y su calidad realmente es mala comparada a VOSK ejemplos de errores:
    #### CUDA (4070 ti super)
    ```
    Whisper thinks you said  probando 1, 2, 3. Ah bueno, si lo hará detectarlo correctamente. 
    Say something!
    Whisper thinks you said  Eso, Cooking All is you
    Say something!
    Whisper thinks you said  Es que lo corrige, pues, como es la voz que se corregía automáticamente.
    Say something!
    Whisper thinks you said  que me consume ak oak castanmente 920derram.
    Say something!
    UDA, creo que es la mayor cosa, yo tengo CUDA y eso es lo que CUDA directamente, es que como está el decodificando video cuando no debería y además mira aumentado el consumo de beta RAM, o sea tipo está usando CUDA, pues es muy rápido pero si yo le dijese para que usara únicamente sólo metes CPU creo que ahí cambiaría la cosa, voy a verificar si lo puedo obligar a que utiliza nada más CPU
    Say something!
    Whisper thinks you said
    Say something!
    Whisper thinks you said  No, va a ser la propia librería de speech, recondicción.
    Say something!
    Whisper thinks you said  esto ya va a poner false creo que con esto lo voy a obligar a que mira que está a bosque también hay que tener para vosotros por bosque mucho mejor whisper tensor flow ah también existentensor flow no pero también son pesados y bm pero creo que estáis de aquí si es de aquí
    ```
    #### CPU (i7-11700f)
    ```
    Say something!
    Whisper thinks you said  Imagínate que signo que los pueda.
    Say something!
    Whisper thinks you said  ahora sí, ahora sí está empezándolo cuando, mira, mira, mira, mira, mira
    Say something!
    Whisper thinks you said  para verme vos utiliza hasta un 22% de ese peo.
    Say something!
    Whisper thinks you said  pero también creo que ahí también un 26% de jefe o también la loco está en mismo tiempo
    Say something!
    Whisper thinks you said  ¡Cheer! ¡Cheer!
    Say something!
    ```
    #### Codigo
    ```python
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
          print("Whisper thinks you said " + r.recognize_whisper(audio, language="spanish"))
      except sr.UnknownValueError:
          print("Whisper could not understand audio")
      except sr.RequestError as e:
          print(f"Could not request results from Whisper; {e}")
    ```


- ~~Alternativa~~
  - ~~https://github.com/Purfview/whisper-standalone-win es linea de comandos pero no soporta microfono~~
  - ~~Usar SpeechRecognition para manipularlo lo hace mas "simple" pero igual requiere 3 dependencias~~
