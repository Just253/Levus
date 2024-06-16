import tkinter as tk
import screen_ocr 
import time

root = tk.Tk()
root.withdraw()

def create_transparent_box(left, top, width, height, number):

    # Crear la ventana transparente
    window = tk.Toplevel()
    window.geometry(f"{width+15}x{height}+{left}+{top}")

    # Quitar la barra de menú de la ventana
    window.overrideredirect(True)

    # Establecer la opacidad de la ventana
    window.attributes("-alpha", 0.5)

    # Establecer el color de fondo de la ventana
    window.config(bg='white')

    # Crear una etiqueta con el número al lado de la caja
    label_match = tk.Label(window, text=str(number), bg='white', fg='black', font=('Arial', 12, 'bold'))
    label_match.place(relx=1.0, rely=0.5,anchor='e')

    # Mostrar la ventana
    window.deiconify()

    return window

# Crear un lector de OCR
ocr_reader = screen_ocr.Reader.create_quality_reader()

# Leer la pantalla
results = ocr_reader.read_screen()

# Buscar las palabras que coinciden con "hola"
matches = results.find_matching_words("hola")

# Crear una ventana para cada coincidencia
windows = []
for i, match in enumerate(matches, start=1):
    # Verificar si match es una lista y acceder correctamente a los atributos
    if isinstance(match, list) and len(match) > 0:
        left = match[0].left
        top = match[0].top
        width = match[0].width
        height = match[0].height
        window = create_transparent_box(left, top, width, height, i)
        windows.append(window)

# Mantener el script en ejecución hasta que todas las ventanas se cierren
while windows:
    windows = [window for window in windows if window.winfo_exists()]
    root.update()
    time.sleep(1)

root.mainloop()