import tkinter as tk
import screen_ocr
import time

root = tk.Tk()
root.withdraw() 
def create_transparent_box(match, number):
    # Crea una ventana
    window = tk.Toplevel()
    window.geometry(f"{match.width}x{match.height}+{match.left}+{match.top}")
    # Quita la barra de menú de la ventana
    window.overrideredirect(True)
    # Establece la opacidad de la ventana
    window.attributes("-alpha", 0.5)
    # Establece el color de fondo de la ventana
    window.config(bg='red')
    # Crea una etiqueta con el número en el centro de la ventana
    label = tk.Label(window, text=str(number), bg='red', fg='white')
    label.pack(expand=True, fill='both')
    # Muestra la ventana
    window.deiconify()
    return window
# Crea un lector de OCR
ocr_reader = screen_ocr.Reader.create_quality_reader()
# Lee la pantalla
results = ocr_reader.read_screen()
# Busca las palabras que coinciden con "Java"
matches = results.find_matching_words("Java")
# Crea una ventana para cada coincidencia
windows = [create_transparent_box(match[0], i) for i, match in enumerate(matches, start=1)]

# Mantén el script en ejecución hasta que todas las ventanas se cierren
# # Oculta la ventana principal
while windows:
    windows = [window for window in windows if window.winfo_exists()]
    root.update()
    time.sleep(1)