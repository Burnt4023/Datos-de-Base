import sqlite3 as sql
import tkinter as tk
from PIL import Image, ImageTk
from sql import *

nombres_imagenes_logo = ["Logo1.png", "Logo2.png", "Logo3.png", "Logo4.png", "Logo5.png"]
indice_imagen_logo = 0
imagen_logo_tk = None 

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
    
    
inicializarsql()
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("Datos de Base v0.3")
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

#Botones

# Redimensionar las imágenes


boton_mostrar = tk.Button(ventana, text="Mostrar Cartas", command=mostrar_cartas, compound="top")
boton_añadir = tk.Button(ventana, text="Añadir Carta", command=añadir_carta, compound="top")
boton_borrar = tk.Button(ventana, text="Borrar Carta", command=borrar_carta, compound="top")
boton_buscar = tk.Button(ventana, text="Buscar Carta", command=buscar_carta, compound="top")
# Posicionamiento de los botones (ajusta según tus necesidades)
boton_mostrar.place(x=150, y=200)
boton_añadir.place(x=350, y=200)
boton_borrar.place(x=550, y=200)
boton_buscar.place(x=350, y=300)
cambiar_logo()

ventana.mainloop()
