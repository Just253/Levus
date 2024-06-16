# Levus 

## Descripción
El proyecto se basa en un controlador de computadora basado en voz y gestos, donde se utilizarán bibliotecas para reconocimiento de voz, texto a voz, reconocimiento de manos, inteligencia artificial de código abierto. El controlador tendrá muchos comandos, como abrir aplicaciones según la configuración, crear comandos personalizados y más con la ayuda de la IA. Ahora, el proyecto no solo se basa en Python, sino también en Java. Java se utilizará para la interfaz gráfica de usuario (GUI), mientras que Python se utilizará para el servidor donde se administran los comandos, la conexión con la IA, el reconocimiento, etc. La GUI de Java tiene como objetivo simplificar las cosas y hacerlas más fáciles de usar.

## Estructura del Proyecto
```
Levus
 │   .gitignore
 │   config.json 
 │   start.bash
 │   start.bat
 ├───app
 │   ├─src
 │   │  ├─main
 │   │  │  ├─java
 │   │  │  │  └─levus
 |   |  ...
 └───server
     ├───api
     ├───commands
     └───models
```

## Configuración
El archivo `config.json` es donde esperamos configurar las distintas opciones del proyecto. Por ejemplo, la ruta de diferentes carpetas (modelos, comandos, etc.), el idioma de la IA, el idioma de la voz, etc. Ademas limitar el consumo de javaFX con la memoria RAM.

## Iniciar el Proyecto
Para iniciar el proyecto, simplemente ejecute el archivo `start.bash` en Linux o `start.bat` en Windows. Este archivo se encargará de iniciar el servidor y la interfaz gráfica de usuario.

# Registro de Cambios
#### ...

# Lista de Tareas
...

# Agradecimientos

Este proyecto utiliza "hand-gesture-recognition-using-mediapipe" de Shigeki Takahashi. Si utilizas este proyecto en tu investigación, por favor cítalo usando la siguiente referencia:

Takahashi, S. (2020). hand-gesture-recognition-using-mediapipe. Recuperado de https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe