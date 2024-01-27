import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def inicializarsql():
    connection = sql.connect("Kebab.db")
    cursor = connection.cursor()
    
    TablaKebab = """CREATE TABLE IF NOT EXISTS Kebab (
        ID INTEGER PRIMARY KEY,
        Kebaberia TEXT,
        Precio FLOAT,
        Nota INTEGER,
        Cantidad INTEGER
    );"""
    
    cursor.execute(TablaKebab)
    connection.commit()
    connection.close()


def mostrar_kebabs():
    ventana_mostrar = tk.Tk()
    ventana_mostrar.geometry("800x400")
    ventana_mostrar.title("Datos de Base v0.3")
    ventana_mostrar.resizable(False, True)
    ventana_mostrar.iconbitmap("assets/elpepe.ico")

    # Crear un Treeview para mostrar los datos de los kebabs
    tree = ttk.Treeview(ventana_mostrar, columns=("ID", "Kebaberia", "Precio", "Nota", "Cantidad"), show="headings")

    # Definir encabezados de columnas
    tree.heading("ID", text="ID")
    tree.heading("Kebaberia", text="Kebaberia")
    tree.heading("Precio", text="Precio")
    tree.heading("Nota", text="Nota")
    tree.heading("Cantidad", text="Cantidad")

    # Ajustar el ancho de las columnas
    tree.column("ID", width=40, anchor="center")
    tree.column("Kebaberia", width=120)
    tree.column("Precio", width=80, anchor="center")
    tree.column("Nota", width=60, anchor="center")
    tree.column("Cantidad", width=80, anchor="center")

    # Conectar a la base de datos y obtener los datos de los kebabs
    connection = sql.connect("Kebab.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Kebab")
    kebabs = cursor.fetchall()
    connection.close()

    # Insertar los datos en el Treeview
    for kebab in kebabs:
        tree.insert("", "end", values=kebab)

    # Empaquetar el Treeview
    tree.pack(fill="both", expand=True)
    # Cerrar la ventana después de mostrar los kebabs
    ventana_mostrar.mainloop()
    

def anadir_kebab():
    ventana_anadir = tk.Tk()
    ventana_anadir.geometry("300x200")
    ventana_anadir.title("Datos de Base v0.3")
    ventana_anadir.iconbitmap("assets/elpepe.ico")

    label_kebaberia = tk.Label(ventana_anadir, text="Kebaberia:")
    entry_kebaberia = tk.Entry(ventana_anadir)

    label_precio = tk.Label(ventana_anadir, text="Precio:")
    entry_precio = tk.Entry(ventana_anadir)

    label_nota = tk.Label(ventana_anadir, text="Nota:")
    entry_nota = tk.Entry(ventana_anadir)


    # Función para guardar el nuevo kebab
    def guardar_kebab():
        kebaberia = entry_kebaberia.get()
        precio = entry_precio.get()
        nota = entry_nota.get()

        # Validar que los campos no estén vacíos
        if kebaberia and precio and nota:
            # Conectar a la base de datos y agregar el nuevo kebab
            connection = sql.connect("Kebab.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Kebab (Kebaberia, Precio, Nota, Cantidad) VALUES (?, ?, ?, ?)",
                (kebaberia, precio, nota, 1))
            connection.commit()
            connection.close()

            # Cerrar la ventana después de añadir el kebab
            ventana_anadir.destroy()
        else:
            # Mostrar un mensaje de error si algún campo está vacío
            tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")

    # Botón para guardar el nuevo kebab
    boton_guardar = tk.Button(ventana_anadir, text="Guardar", command=guardar_kebab)

    # Posicionamiento de elementos en la ventana

    label_kebaberia.pack()
    entry_kebaberia.pack()

    label_precio.pack()
    entry_precio.pack()

    label_nota.pack()
    entry_nota.pack()

    boton_guardar.pack()

    ventana_anadir.mainloop()


def editar_kebab():
    ventana_editar = tk.Tk()
    ventana_editar.geometry("600x500")
    ventana_editar.resizable(False, False)
    ventana_editar.title("Datos de Base v0.3")
    ventana_editar.iconbitmap("assets/elpepe.ico")

    label_id = tk.Label(ventana_editar, text="ID del Kebab:")
    entry_id = tk.Entry(ventana_editar)
    
    label_kebaberia = tk.Label(ventana_editar, text="Nueva Kebaberia:")
    entry_kebaberia = tk.Entry(ventana_editar)

    label_precio = tk.Label(ventana_editar, text="Nuevo Precio:")
    entry_precio = tk.Entry(ventana_editar)

    label_nota = tk.Label(ventana_editar, text="Nueva Nota:")
    entry_nota = tk.Entry(ventana_editar)

    label_cantidad = tk.Label(ventana_editar, text="Nueva Cantidad:")
    entry_cantidad = tk.Entry(ventana_editar)

    def cargar_datos():
        # Función para cargar los datos del kebab a editar
        kebab_id = entry_id.get()

        # Conectar a la base de datos y obtener los datos del kebab
        connection = sql.connect("Kebab.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Kebab WHERE ID=?", (kebab_id,))
        kebab = cursor.fetchone()
        connection.close()

        # Mostrar los datos del kebab en los campos de entrada
        entry_kebaberia.insert(0, kebab[1])
        entry_precio.insert(0, kebab[2])
        entry_nota.insert(0, kebab[3])
        entry_cantidad.insert(0, kebab[4])

    def borrar_kebab():
        # Función para borrar el kebab
        kebab_id = entry_id.get()

        # Confirmar la acción con el usuario

        connection = sql.connect("Kebab.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Kebab WHERE ID=?", (kebab_id,))
        connection.commit()
        connection.close()
        entry_id.delete(0, tk.END)  # Limpiar el contenido actual
        entry_id.insert(0, "Borrado!")
        
        
    def guardar_cambios():
        # Función para guardar los cambios realizados en el kebab
        kebab_id = entry_id.get()
        kebaberia = entry_kebaberia.get()
        precio = entry_precio.get()
        nota = entry_nota.get()
        cantidad = entry_cantidad.get()

        # Validar que los campos no estén vacíos

        # Conectar a la base de datos y actualizar el kebab
        connection = sql.connect("Kebab.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE Kebab SET Kebaberia=?, Precio=?, Nota=?, Cantidad=? WHERE ID=?",
                       (kebaberia, precio, nota, cantidad, kebab_id))
        connection.commit()
        connection.close()


    # Botón para cargar datos del kebab
    boton_cargar = tk.Button(ventana_editar, text="Cargar Datos", command=cargar_datos)
    
    # Botón para borrar el kebab
    boton_borrar = tk.Button(ventana_editar, text="Borrar Kebab", command=borrar_kebab)

    # Botón para guardar los cambios
    boton_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios)

    # Posicionamiento de elementos en la ventana
    label_id.pack()
    entry_id.pack()
    
    boton_cargar.pack()
    boton_borrar.pack()

    label_kebaberia.pack()
    entry_kebaberia.pack()

    label_precio.pack()
    entry_precio.pack()

    label_nota.pack()
    entry_nota.pack()

    label_cantidad.pack()
    entry_cantidad.pack()

    boton_guardar.pack()

    ventana_editar.mainloop()