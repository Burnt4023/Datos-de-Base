import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mtgsdk
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


def mostrar_kebabs():
    ventana_mostrar = tk.Tk()
    ventana_mostrar.geometry("800x400")
    ventana_mostrar.title("Datos de Base v0.3")
    ventana_mostrar.resizable(False, True)
    ventana_mostrar.iconbitmap("assets/elpepe.ico")

    # Crear un Treeview para mostrar los datos de los kebabs
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
    kebabs = cursor.fetchall()
    connection.close()

    # Insertar los datos en el Treeview
    for kebab in kebabs:
        tree.insert("", "end", values=kebab)

    # Empaquetar el Treeview
    tree.pack(fill="both", expand=True)
    # Cerrar la ventana después de mostrar los kebabs
    ventana_mostrar.mainloop()
    
def añadir_carta():
    # Función para agregar una carta a la base de datos
    def guardar_carta():
    # Obtener el nombre de la carta ingresado por el usuario
        nombre_carta = entry_nombre.get()

        # Conectar a la base de datos y verificar si la carta ya está presente
        connection = sql.connect("Cartas.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Cartas WHERE Nombre=?", (nombre_carta,))
        existing_carta = cursor.fetchone()

        if existing_carta:
        # Si la carta ya está presente, aumentar la cantidad en 1
            cantidad_actual = existing_carta[4]
            nueva_cantidad = cantidad_actual + 1
            cursor.execute("UPDATE Cartas SET Cantidad=? WHERE Nombre=?", (nueva_cantidad, nombre_carta))
        else:
            # Si la carta no está presente, agregar una nueva entrada
            carta = mtgsdk.Card.where(name=nombre_carta).all()
            if carta:
                carta = carta[0]  # Tomar solo la primera carta si hay múltiples coincidencias
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


    # Crear la ventana para añadir carta
    ventana_añadir_carta = tk.Tk()
    ventana_añadir_carta.title("Añadir Carta")
    ventana_añadir_carta.geometry("400x250")
    ventana_añadir_carta.resizable(False, False)
    
    # Crear etiqueta y campo de texto para ingresar el nombre de la carta
    label_nombre = tk.Label(ventana_añadir_carta, text="Nombre de la carta:")
    entry_nombre = tk.Entry(ventana_añadir_carta)

    # Crear botón para buscar y guardar la carta
    boton_buscar = tk.Button(ventana_añadir_carta, text="Buscar y Guardar", command=guardar_carta)

    # Posicionar elementos en la ventana
    label_nombre.pack()
    entry_nombre.pack()
    boton_buscar.pack()

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
    ventana_borrar.resizable(False, False)
    ventana_borrar.title("Borrar Carta")

    label_nombre = tk.Label(ventana_borrar, text="Nombre de la carta:")
    label_nombre.pack()

    entry_nombre = tk.Entry(ventana_borrar)
    entry_nombre.pack()

    boton_borrar = tk.Button(ventana_borrar, text="Borrar", command=borrar)
    boton_borrar.pack()

    ventana_borrar.mainloop()
    

def buscar_carta():
    # Función para buscar la carta y mostrar sus datos
    
    def mostrar_datos():
    # Función para mostrar los datos de la carta
    
    # Conectar a la base de datos y obtener los datos de la carta
        connection = sql.connect("Cartas.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Cartas WHERE Nombre=?", (entry_nombre.get(),))
        datos_carta = cursor.fetchone()
        connection.close()
    
    # Limpiar el contenido actual de la ventana
        for widget in ventana_buscar.winfo_children():
           widget.destroy()
    
    # Verificar si la carta se encontró en la base de datos
        if datos_carta:
            # Crear un Treeview para mostrar los datos de la carta
            tree = ttk.Treeview(ventana_buscar, columns=("Nombre", "Tipo", "Coste", "Poder", "Cantidad"), show="headings")
            # Definir encabezados de columnas
            tree.heading("Nombre", text="Nombre")
            tree.heading("Tipo", text="Tipo")
            tree.heading("Coste", text="Coste")
            tree.heading("Poder", text="Poder")
            tree.heading("Cantidad", text="Cantidad")
            tree.column("Nombre", width=40, anchor="center")
            tree.column("Tipo", width=120, anchor = "center")
            tree.column("Coste", width=80, anchor="center")
            tree.column("Poder", width=60, anchor="center")
            tree.column("Cantidad", width=80, anchor="center")

            # Insertar los datos de la carta en el Treeview
            tree.insert("", "end", values=datos_carta)
        
            # Empaquetar el Treeview
            tree.pack(fill="both", expand=True)
        else:
            # Mostrar un mensaje indicando que la carta no fue encontrada
            etiqueta_no_encontrada = tk.Label(ventana_buscar, text="Carta no encontrada")
            etiqueta_no_encontrada.pack()
            entry_nombre = tk.Entry(ventana_buscar)
            entry_nombre.pack()
            boton_mostrar_datos = tk.Button(ventana_buscar, text="Mostrar Datos", command=mostrar_datos)
            boton_mostrar_datos.pack()
    
    # Crear la ventana para buscar la carta
    ventana_buscar = tk.Tk()
    ventana_buscar.title("Buscar Carta")
    ventana_buscar.geometry("700x300")
    ventana_buscar.resizable(False, False)
    # Campo de entrada para el nombre de la carta
    label_nombre = tk.Label(ventana_buscar, text="Nombre de la carta:")
    label_nombre.pack()
    entry_nombre = tk.Entry(ventana_buscar)
    entry_nombre.pack()
    
    # Botón para mostrar los datos de la carta
    boton_mostrar_datos = tk.Button(ventana_buscar, text="Mostrar Datos", command=mostrar_datos)
    boton_mostrar_datos.pack()
    
    # Ejecutar el bucle principal de la ventana
    ventana_buscar.mainloop()