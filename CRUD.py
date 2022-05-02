from tkinter import *
from tkinter import messagebox
import sqlite3

#-------------Funciones----------------------------------------
#Post: Crea la conexion a la BBBDD, si esta ya existe devuelve un warning
def conexionBBDD():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE DATOSUSUARIOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(20),
            APELLIDO VARCHAR(20),
            DIRECCION VARCHAR(20),
            COMENTARIOS VARCHAR(100))
            ''')

        messagebox.showinfo("BBDD", "BBDD creada con exito")
    except:
        messagebox.showwarning("¡Atencion!", "La BBDD ya existe")

#Post: Crea el mensaje de salida si se pulsa en "yes" termina el programa sino no hace nada
def salirApp():
    valor = messagebox.askquestion("Salir", "¿Desea salir de la aplicación?")

    if valor == "yes":
        root.destroy()

def borrarCampos():
    miID.set("")
    miNombre.set("")
    miApellido.set("")
    miPassword.set("")
    miDireccion.set("")
    cuadroComentarios.delete(1.0, END)

#Post: INserta un nuevo registro en nuestra base de datos
def crear():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()

    datos = (miNombre.get(), miApellido.get(), miPassword.get(), miDireccion.get(), cuadroComentarios.get("1.0", END))

    #Forma larga no es conveniente hacerlo asi
    """
    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL, '" + miNombre.get() +
        "','" + miApellido.get() +
        "','" + miPassword.get() +
        "','" + miDireccion.get() +
        "','" + cuadroComentarios.get("1.0", END) + "')")
    """
    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,?,?,?,?,?)", datos) 

    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro insertado con éxito")
        
#Post: Nos muestra por pantalla los datos del id que seleccionamos
def leer():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" + miID.get())

    elUsuario = miCursor.fetchall()
    for usuario in elUsuario:
        miID.set(usuario[0])
        miNombre.set(usuario[1])
        miApellido.set(usuario[2])
        miPassword.set(usuario[3])
        miDireccion.set(usuario[4])
        cuadroComentarios.insert(1.0, usuario[5])

    miConexion.commit()

#Post: Actualiza los campos de un registro, primero se debe leer el registro en el crud y luego actualizarlo
def actualizar():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    
    datos = (miNombre.get(), miApellido.get(), miPassword.get(), miDireccion.get(), cuadroComentarios.get("1.0", END))

    """
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='" + miNombre.get() +
        "', APELLIDO='" + miApellido.get() +
        "', PASSWORD='" + miPassword.get() +
        "', DIRECCION='" + miDireccion.get() +
        "',COMENTARIOS='" + cuadroComentarios.get("1.0", END) + 
        "' WHERE ID=" + miID.get())
    """
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO=?, APELLIDO=?, PASSWORD=?, DIRECCION=?, COMENTARIOS=? " +
        "WHERE ID=" + miID.get(), datos)

    miConexion.commit()
    messagebox.showinfo("BBDD", "Registro actualizado con éxito")

#Post: Elimina un registro de nuestra BBDD
def eliminar():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    
    miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" + miID.get())

    miConexion.commit()
    messagebox.showinfo("BBDD", "Registro borrado con éxito")
    
#------------------------------Parte Grafica------------------------------------
#Pre: Debe recibir el root
#Post: Crea la barra de menu anclada al root
def crearBarraDeMenu(root):
    barraMenu = Menu(root)
    root.config(menu = barraMenu, width = 300, height = 300)

    menuBBDD = Menu(barraMenu, tearoff = 0)
    menuBBDD.add_command(label = "Conectar", command=conexionBBDD)
    menuBBDD.add_command(label = "Salir", command=salirApp)

    menuBorrar = Menu(barraMenu, tearoff = 0)
    menuBorrar.add_command(label = "Borrar campos", command=borrarCampos)

    menuCRUD = Menu(barraMenu, tearoff = 0)
    menuCRUD.add_command(label = "Crear", command=crear)
    menuCRUD.add_command(label = "Leer", command=leer)
    menuCRUD.add_command(label = "Actualizar", command=actualizar)
    menuCRUD.add_command(label = "Borrar", command=eliminar)

    menuAyuda = Menu(barraMenu, tearoff = 0)
    menuAyuda.add_command(label = "Licencia")
    menuAyuda.add_command(label = "Acerca de..")

    barraMenu.add_cascade(label = "BBDD", menu = menuBBDD)
    barraMenu.add_cascade(label = "Borrar", menu = menuBorrar)
    barraMenu.add_cascade(label = "CRUD", menu = menuCRUD)
    barraMenu.add_cascade(label = "Ayuda", menu = menuAyuda)

#Pre: Recibe el frame superior
#Post: Crea los labels en el frame superior
def crearLabels(frame):
    idLabel = Label(miFrame, text = "ID:")
    idLabel.grid(row = 0, column = 0, sticky = "e", padx = 10, pady = 10)

    nombreLabel = Label(miFrame, text = "Nombre:")
    nombreLabel.grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 10)

    apellidoLabel = Label(miFrame, text = "Apellido:")
    apellidoLabel.grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 10)

    passwordLabel = Label(miFrame, text = "Password:")
    passwordLabel.grid(row = 3, column = 0, sticky = "e", padx = 10, pady = 10)

    direccionLabel = Label(miFrame, text = "Direccion:")
    direccionLabel.grid(row = 4, column = 0, sticky = "e", padx = 10, pady = 10)

    comentariosLabel = Label(miFrame, text = "Comentarios:")
    comentariosLabel.grid(row = 5, column = 0, sticky = "e", padx = 10, pady = 10)

#Pre: Recibe el frame superior
#Post: Crea los entrys en el frame superior
def crearEntrys(frame):

    cuadroID = Entry(miFrame, textvariable=miID)
    cuadroID.grid(row = 0, column = 1, padx = 10, pady = 10)

    cuadroNombre = Entry(miFrame, textvariable=miNombre)
    cuadroNombre.grid(row = 1, column = 1, padx = 10, pady = 10)

    cuadroApellido = Entry(miFrame, textvariable=miApellido)
    cuadroApellido.grid(row = 2, column = 1, padx = 10, pady = 10)

    cuadroPassword = Entry(miFrame, textvariable=miPassword)
    cuadroPassword.grid(row = 3, column = 1, padx = 10, pady = 10)
    cuadroPassword.config(show = "*")

    cuadroDireccion = Entry(miFrame, textvariable=miDireccion)
    cuadroDireccion.grid(row = 4, column = 1, padx = 10, pady = 10)


#Pre: Recibe el frame inferior
#Post: Crea los Buttons en el frame inferior
def crearButtons(frameInferior):
    botonCreate = Button(frameInferior, text = "Create", width = 5, command=crear)
    botonCreate.grid(row = 1, column = 0, sticky = "w", padx = 10, pady = 10)

    botonRead = Button(frameInferior, text = "Read", width = 5, command=leer)
    botonRead.grid(row = 1, column = 1, sticky = "w", padx = 10, pady = 10)

    botonUpdate = Button(frameInferior, text = "Update", width = 5, command=actualizar)
    botonUpdate.grid(row = 1, column = 2, sticky = "w", padx = 10, pady = 10)

    botonDelete = Button(frameInferior, text = "Delete", width = 5, command=eliminar)
    botonDelete.grid(row = 1, column = 3, sticky = "w", padx = 10, pady = 10)

#Raiz
root = Tk()
root.title("CRUD")

#Frame
miFrame = Frame(root, width = 400, height = 400)
miFrame.pack()

#Barra de menu
crearBarraDeMenu(root)

#Labels
crearLabels(miFrame)

#Entrys
miID = StringVar()
miNombre = StringVar()
miApellido = StringVar()
miPassword = StringVar()
miDireccion = StringVar()

crearEntrys(miFrame)

#cuadro de comentarios
cuadroComentarios = Text(miFrame, width = 16, height = 5)
cuadroComentarios.grid(row = 5, column = 1, padx = 10, pady = 10)

#ScrollBar para el cuadro de comentarios
scrollVertical = Scrollbar(miFrame, command = cuadroComentarios.yview)
scrollVertical.grid(row = 5, column = 2, sticky = "nsew")
cuadroComentarios.config(yscrollcommand = scrollVertical.set)

#Frame para los botones inferiores
frameInferior = Frame(root)
frameInferior.pack()

#Buttons
crearButtons(frameInferior)

root.mainloop()