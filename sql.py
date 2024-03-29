import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
import mtgsdk
from PIL import ImageTk, Image
import os

posicion_ventana = None

def inicializarsql():
    connection = sql.connect("Cartas.db")
    cursor = connection.cursor()
    
    TablaCartas = """CREATE TABLE IF NOT EXISTS Cartas (
        Nombre TEXT PRIMARY KEY,
        Tipo TEXT,
        Coste FLOAT,
        Poder TEXT,
        Cantidad INTEGER
    );"""
    
    cursor.execute(TablaCartas)
    connection.commit()
    connection.close()


def mostrar_cartas():
    def recargar_ventana(event):
        ventana_mostrar.destroy()
        mostrar_cartas()
    ventana_mostrar = tk.Tk()
    ventana_mostrar.geometry("800x400")
    ventana_mostrar.title("Datos de Base v0.3")
    ventana_mostrar.iconbitmap("assets/elpepe.ico")

    # Crear un Treeview para mostrar los datos de las cartas
    tree = ttk.Treeview(ventana_mostrar, columns=("Nombre", "Tipo", "Coste", "Poder", "Cantidad"), show="headings")

    # Definir encabezados de columnas
    tree.heading("Nombre", text="Nombre")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Coste", text="Coste")
    tree.heading("Poder", text="Poder")
    tree.heading("Cantidad", text="Cantidad")

    # Ajustar el ancho de las columnas
    tree.column("Nombre", width=40, anchor="center")
    tree.column("Tipo", width=120, anchor = "center")
    tree.column("Coste", width=80, anchor="center")
    tree.column("Poder", width=60, anchor="center")
    tree.column("Cantidad", width=80, anchor="center")

    # Conectar a la base de datos y obtener los datos de los kebabs
    connection = sql.connect("Cartas.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Cartas")
    cartas = cursor.fetchall()
    connection.close()

    # Insertar los datos en el Treeview
    for carta in cartas:
        tree.insert("", "end", values=carta)

    # Empaquetar el Treeview
    tree.pack(fill="both", expand=True)
    ventana_mostrar.bind("<F5>", recargar_ventana)
    # Cerrar la ventana después de mostrar las cartas
    ventana_mostrar.mainloop()
    
def añadir_carta():
    def guardar_carta():
    # Obtener el nombre de la carta ingresado por el usuario
        nombre_carta = entry_nombre.get()
        idioma_seleccionado = combo_idioma.get()

    # Buscar la carta en mtgsdk con el idioma seleccionado
        if idioma_seleccionado == "English":
            carta = mtgsdk.Card.where(name=nombre_carta).all()
        else:
            carta = mtgsdk.Card.where(name=nombre_carta, language=idioma_seleccionado).all()

        if carta:
            carta = carta[0]  # Tomar solo la primera carta si hay múltiples coincidencias

        # Conectar a la base de datos y verificar si la carta ya está presente
            connection = sql.connect("Cartas.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Cartas WHERE Nombre=?", (carta.name,))
            existing_carta = cursor.fetchone()

            if existing_carta:
            # Si la carta ya está presente, aumentar la cantidad en 1
                nueva_cantidad = existing_carta[4] + 1  # Asumiendo que la cantidad está en la posición 5
                cursor.execute("UPDATE Cartas SET Cantidad=? WHERE Nombre=?", (nueva_cantidad, carta.name))
            else:
            # Si la carta no está presente, agregar una nueva entrada
                nombre = carta.name
                tipo = carta.type
                coste = carta.cmc
                if "creature" in carta.type.lower():
                    poder_resistencia = f"{carta.power}/{carta.toughness}" if carta.power and carta.toughness else "N/A"
                else:
                    poder_resistencia = "N/A"
                cantidad = 1  # Por defecto, se añade una carta

                cursor.execute("INSERT INTO Cartas (Nombre, Tipo, Coste, Poder, Cantidad) VALUES (?, ?, ?, ?, ?)",
                           (nombre, tipo, coste, poder_resistencia, cantidad))
        
            connection.commit()
            connection.close()
        else:
            print("Carta no encontrada en el idioma seleccionado.")

    # Crear la ventana para añadir carta
    ventana_añadir_carta = tk.Tk()
    ventana_añadir_carta.title("Añadir Carta")
    ventana_añadir_carta.iconbitmap("assets/elpepe.ico")
    ventana_añadir_carta.geometry("400x250")
    
    # Crear etiqueta y campo de texto para ingresar el nombre de la carta
    label_nombre = tk.Label(ventana_añadir_carta, text="Nombre de la carta:")
    entry_nombre = tk.Entry(ventana_añadir_carta)

    # Crear combobox para seleccionar el idioma
    idiomas = ["Spanish", "English"]  # Opcional: Puedes añadir más idiomas si lo deseas
    combo_idioma = ttk.Combobox(ventana_añadir_carta, values=idiomas, state="readonly")
    combo_idioma.current(0)  # Establecer el idioma por defecto

    # Crear botón para buscar y guardar la carta
    boton_buscar = tk.Button(ventana_añadir_carta, text="Buscar y Guardar", command=guardar_carta)

    # Posicionar elementos en la ventana
    label_nombre.pack()
    entry_nombre.pack()
    combo_idioma.pack(pady=10)
    boton_buscar.pack(pady=10)

    # Ejecutar la ventana
    ventana_añadir_carta.mainloop()
    
def borrar_carta():
    def borrar():
        label_nombre.config(text="Nombre de la carta")
        nombre_carta = entry_nombre.get()
        
        if nombre_carta:
            # Conectar a la base de datos
            connection = sql.connect("Cartas.db")
            cursor = connection.cursor()

            # Verificar si la carta ya está en la base de datos
            cursor.execute("SELECT * FROM Cartas WHERE Nombre=?", (nombre_carta,))
            carta_existente = cursor.fetchone()

            if carta_existente:
                cantidad = carta_existente[4]  # Obtener la cantidad actual de la carta
                if cantidad > 1:
                    # Si hay más de una carta, disminuir la cantidad en 1
                    cursor.execute("UPDATE Cartas SET Cantidad=? WHERE Nombre=?", (cantidad - 1, nombre_carta))
                    connection.commit()
                else:
                    # Si hay solo una carta, eliminarla de la base de datos
                    cursor.execute("DELETE FROM Cartas WHERE Nombre=?", (nombre_carta,))
                    connection.commit()
            else: 
                label_nombre.config(text="Carta no encontrada")

            # Cerrar la conexión a la base de datos
            connection.close()

    ventana_borrar = tk.Tk()
    ventana_borrar.geometry("400x250")
    ventana_borrar.iconbitmap("assets/elpepe.ico")
    ventana_borrar.title("Borrar Carta")

    label_nombre = tk.Label(ventana_borrar, text="Nombre de la carta:")
    label_nombre.pack()

    entry_nombre = tk.Entry(ventana_borrar)
    entry_nombre.pack()

    boton_borrar = tk.Button(ventana_borrar, text="Borrar", command=borrar)
    boton_borrar.pack()

    ventana_borrar.mainloop()
    

def buscar_carta():
    def mostrar_datos(entry_nombre, tree):
        nombre_carta = entry_nombre.get()
        idioma = combo_idioma.get()
        for item in tree.get_children():
            tree.delete(item)
        if idioma != "English":
            carta = mtgsdk.Card.where(name=nombre_carta, language=idioma).all()[0]
        else:
            carta = mtgsdk.Card.where(name=nombre_carta).all()[0]

        connection = sql.connect("Cartas.db")
        cursor = connection.cursor()
        cursor.execute("SELECT Cantidad FROM Cartas WHERE Nombre=?", (carta.name,))
        cantidad_cartas = cursor.fetchone()
        connection.close()
        
        if cantidad_cartas:
            cantidad = cantidad_cartas[0]  # Corrección aquí, la cantidad está en la primera posición
        else:
            cantidad = 0
        
        # Consideramos el idioma al buscar la carta

        
        if carta:
            if "Creature" not in carta.type:
                carta.power = "N/A"
            tree.insert("", "end", values=(carta.name, carta.type, carta.cmc, carta.power, cantidad))
        else:
            tree.insert("", "end", values=("Carta no encontrada", "", "", "", ""))
    
    def recargar_ventana(event):
        ventana_buscar.destroy()
        buscar_carta()
    
    
    ventana_buscar = tk.Tk()
    ventana_buscar.title("Buscar Carta")
    ventana_buscar.iconbitmap("assets/elpepe.ico")
    ventana_buscar.geometry("500x350")
    
    tree = ttk.Treeview(ventana_buscar, columns=("Nombre", "Tipo", "Coste", "Poder", "Cantidad"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Coste", text="Coste")
    tree.heading("Poder", text="Poder")
    tree.heading("Cantidad", text="Cantidad")

    # Ajustar el ancho de las columnas
    tree.column("Nombre", width=160, anchor="center")
    tree.column("Tipo", width=160, anchor = "center")
    tree.column("Coste", width=50, anchor="center")
    tree.column("Poder", width=50, anchor="center")
    tree.column("Cantidad", width=80, anchor="center")
    tree.pack()
    
    label_nombre = tk.Label(ventana_buscar, text="Nombre de la carta:")
    label_nombre.pack()
    
    idiomas = ["Spanish", "English"]
    combo_idioma = ttk.Combobox(ventana_buscar, values=idiomas, state="readonly")
    combo_idioma.current(0)  # Establecer el idioma por defecto
    combo_idioma.pack(pady=10)
    
    entry_nombre = tk.Entry(ventana_buscar)
    entry_nombre.pack()
    
    boton_mostrar_datos = tk.Button(ventana_buscar, text="Mostrar Datos", command=lambda: mostrar_datos(entry_nombre, tree))
    boton_mostrar_datos.pack()
    
    ventana_buscar.bind("<F5>", recargar_ventana)
    ventana_buscar.mainloop()