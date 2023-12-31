# Levus 
## Descripción
El proyecto se basa en un controlador de computadora basado en voz y gestos, donde se utilizarán bibliotecas para reconocimiento de voz, texto a voz, reconomiento de manos, inteligencia artificial de código abierto y OCR para la detección de letras según la ventana de una aplicación. El controlador tendrá muchos comandos, como abrir aplicaciones según la configuración, crear comandos personalizados y más con la ayuda de la IA.



## Instrucciones de instalación
```shell	
pip install -r requirements.txt
```

## Lista de tareas pendientes
- [X] Implementar reconocimiento de voz.
- [X] Hacer un gestor de eventos de comandos.
- [X] Usar los servicios gratuitos de IA gracias a [GTP4free](https://github.com/xtekky/gpt4free)
- [X] Implementar texto a voz.
- [X] Crear comandos personalizados a partir de voz.
- [ ] Implementar reconocimiento de gestos.
- [ ] Hacer una GUI
- [ ] Implementar OCR para la detección de letras (segun aplicaciones o pantalla completa).
- [ ] Abrir aplicaciones según la configuración.
- [ ] Comandos predefinidos, como abrir una aplicación o comando.
## Registro de cambios
- Versión 0.1: Creación del repo y planificacion

> - (22/10/23) Traducir [Annyang](https://github.com/TalAter/annyang) a python e implementarlo
> - (23/10/23) Mejorar el class Annyang ahora llamado AnnyangV2 e integrado correctamente
> - (24/10/23) Crear eventCommandHandler que administra los cambios en la carpeta comandos para actualizar la lista de comandos si es necesario.
> - ~~(25/10/23) Traducir los bots de [ChatAll](https://github.com/sunner/ChatALL/) a python e implementarlo~~
> - (28/10/23) Implementar [GTP4free](https://github.com/xtekky/gpt4free) y en paralelo buscar proyectos de reconocimiento de gestos para implementarlo en los siguientes dias.
> - (29/10/23) Preparar el class Levus para unir la IA con AnnyangV2 (Reconocimiento de voz)
> - (08/11/23) Añadido conexion con la IA para crear comandos, nuevos metodos y atributos en Levus para futuras modificaciones, corregido algunos errores con el reconomiento de voz. 

- Versión 0.2:
> - ...