import sqlite3 as sql
import tkinter as tk
from PIL import Image, ImageTk

# Animación
nombres_imagenes_logo = ["Logo1.png", "Logo2.png", "Logo3.png", "Logo4.png", "Logo5.png"]
indice_imagen_logo = 0
imagen_logo_tk = None  # Mantener una referencia global

def cambiar_logo():
    global indice_imagen_logo, imagen_logo_tk
    if indice_imagen_logo < len(nombres_imagenes_logo):
        imagen_logo = Image.open(f"assets/{nombres_imagenes_logo[indice_imagen_logo]}").convert("RGBA")
        imagen_logo_tk = ImageTk.PhotoImage(imagen_logo)
        canvas.itemconfig(logo_canvas, image=imagen_logo_tk)
        indice_imagen_logo += 1
        if indice_imagen_logo == len(nombres_imagenes_logo):
            indice_imagen_logo = 0
        ventana.after(60, cambiar_logo)  # Cambia cada segundo (ajusta según tus necesidades)

# Abre la Base de Datos y prepara el cursor
conect = sql.connect("Datos.db")
cursor = conect.cursor()

# Creación de la ventana (800x600 no reescalable)
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.resizable(False, False)
ventana.title("Datos de Base v0.1")
ventana.iconbitmap("assets/elpepe.ico")

canvas = tk.Canvas(ventana, width=800, height=600, highlightthickness=0)
canvas.pack()

# Mostrar la imagen de fondo en el Canvas
imagen_fondo = Image.open("assets/Fondo.jpg")
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
fondo_canvas = canvas.create_image(400, 300, anchor="center", image=imagen_fondo)  # Ajusta la posición de fondo

# Mostrar la imagen de logo en el Canvas
imagen_logo = Image.open(f"assets/{nombres_imagenes_logo[indice_imagen_logo]}").convert("RGBA")
imagen_logo_tk = ImageTk.PhotoImage(imagen_logo)
logo_canvas = canvas.create_image(400, 0, anchor="n", image=imagen_logo_tk)  # Ajusta la posición del logo

# Iniciar el cambio de imágenes de logo
cambiar_logo()

# Cerrar la conexión y ventana al cerrar la aplicación
ventana.protocol("WM_DELETE_WINDOW", lambda: (conect.close(), ventana.destroy()))

ventana.mainloop()
conect.close()