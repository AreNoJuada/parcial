#Solucion del proyecto (Jeremy zuleta Galvis, Juan David Arenas Nohava)

#Inicialmente, importamos las bibliotecas que se trabajaron en clase junto a otras
#bibliotecas estandares de python:
from tkinter import Tk, Label, Entry, Button, StringVar, Menu
from tkinter.ttk import Treeview, OptionMenu, Menubutton

#Creamos la ventana principal
root = Tk()
root.title("Simulador de ventas")
root.geometry("400x400")

#Lista de productos que gestiona el inventario
inventario = []

#Definimos las variables para capturar las entradas del usuario
nombre_producto = StringVar()
precio_producto = StringVar()
cantidad_producto = StringVar()
producto_seleccionado = StringVar()

#Construimos funcion para agregar un producto al inventario
def agregar_producto():
    try:
        nombre = nombre_producto.get()
        precio = float(precio_producto.get())
        cantidad = int(cantidad_producto.get())

        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        
        inventario.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
        actualizar_menu()
        resultado_label.config(text=f"Producto '{nombre}' El producto fue agregado exitosamente.")
    except ValueError as e:
        resultado_label.config(text=f"Hay un Error: {e}")

#Construimos una funcion para mostrar los detalles del producto seleccionado
def mostrar_detalles_producto():
    for producto in inventario:
        if producto["nombre"] == producto_seleccionado.get():
            resultado_label.config(
                text=f"Producto: {producto['nombre']}\nPrecio: ${producto['precio']:.2f}\nCantidad: {producto['cantidad']}"
            )
            return
    resultado_label.config(text="Error: El producto no ha sido encontrado.")

# Construimos una función para eliminar el producto seleccionado
def eliminar_producto():
    global inventario
    inventario = [p for p in inventario if p["nombre"] != producto_seleccionado.get()]
    actualizar_menu()
    resultado_label.config(text=f"El producto se elimino.")

#Construimos una funcion para actualizar las opciones del menu
def actualizar_menu():
    menu_opciones = [p["nombre"] for p in inventario]
    if menu_opciones:
        producto_seleccionado.set(menu_opciones[0])
        opcion_menu["menu"].delete(0, "end")
        for opcion in menu_opciones:
            opcion_menu["menu"].add_command(
                label=opcion, command=lambda value=opcion: producto_seleccionado.set(value)
            )
    else:
        producto_seleccionado.set("")
        opcion_menu["menu"].delete(0, "end")

#############################################
########### PARTE NO ORGANIZADA ###############
#############################################

# Widgets para agregar productos
Label(root, text="Nombre del Producto:").pack(pady=5)
Entry(root, textvariable=nombre_producto).pack()

Label(root, text="Precio del Producto:").pack(pady=5)
Entry(root, textvariable=precio_producto).pack()

Label(root, text="Cantidad del Producto:").pack(pady=5)
Entry(root, textvariable=cantidad_producto).pack()

Button(root, text="Agregar Producto", command=agregar_producto).pack(pady=10)

# Widget para seleccionar un producto
Label(root, text="Seleccionar Producto:").pack(pady=5)
opcion_menu = OptionMenu(root, producto_seleccionado, "")
opcion_menu.pack()

# Botones para acciones sobre productos
Button(root, text="Mostrar Detalles", command=mostrar_detalles_producto).pack(pady=5)
Button(root, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)

# Etiqueta para mostrar resultados o mensajes
resultado_label = Label(root, text="")
resultado_label.pack(pady=20)

# Iniciar la aplicación
root.mainloop()

    