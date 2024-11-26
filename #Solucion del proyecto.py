#Solucion del proyecto (Jeremy zuleta Galvis, Juan David Arenas Nohava)

#Inicialmente, importamos las bibliotecas que se trabajaron en clase junto a otras
#bibliotecas estandares de python:
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, StringVar, Menu, Toplevel
from tkinter.ttk import Treeview, OptionMenu, Menubutton, Frame

#Ventana principal
root = Tk()
root.title("Simulador de ventas")
root.geometry("1000x480+100+100")
root.configure(background='#D8D8D8')


### frame dentro de la ventana ###
frame1=tk.Frame(root, bg='#484848')
frame1.pack(expand=True, fill='both', side='left')
frame1.config(border='26')
frame1.config(width='50', height='50')

frame2=tk.Frame(root, bg='lightblue')
frame2.pack(expand=True, fill='both', side='right')
frame2.config(border='25', relief='sunken')

frame3=tk.Frame(root,bg='#42A5F5')
frame3.place(x=550, y=300)
frame3.config(width=200, height=100)


#Lista de productos que gestiona el inventario
inventario = []

#Definimos las variables para capturar las entradas del usuario
nombre_producto = StringVar()
precio_producto = StringVar()
cantidad_producto = StringVar()
producto_seleccionado = StringVar()


# Lista global para registrar las ventas
historial_ventas = []

# Ventana secundaria para el historial de ventas
def ventana_secundaria():
    # Crear una ventana Toplevel (hija de root)
    ventana_historial = Toplevel(root)
    ventana_historial.title("Historial de Ventas")
    ventana_historial.geometry("800x500")
    ventana_historial.configure(background='#F5F5F5')

    # Título
    titulo = Label(ventana_historial, text="Historial de Ventas", bg='#F5F5F5', fg='black', font=("Arial", 14))
    titulo.pack(pady=10)

    # Crear un Treeview para mostrar las ventas
    columnas = ("Producto", "Precio", "Cantidad", "Total")
    tree = Treeview(ventana_historial, columns=columnas, show='headings')
    tree.heading("Producto", text="Producto")
    tree.heading("Precio", text="Precio")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Total", text="Total")
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # Agregar datos del historial al Treeview
    for venta in historial_ventas:
        tree.insert("", "end", values=(venta["producto"], f"${venta['precio']:.2f}", venta["cantidad"], f"${venta['total']:.2f}"))

    # Mostrar el producto más vendido
    producto_mas_vendido_label = Label(ventana_historial, text="", bg='#F5F5F5')
    producto_mas_vendido_label.pack(pady=10)

    # Calcular y mostrar el producto más vendido
    if historial_ventas:
        producto_mas_vendido = calcular_producto_mas_vendido()
        producto_mas_vendido_label.config(
            text=f"Producto más vendido: {producto_mas_vendido['producto']} - {producto_mas_vendido['cantidad']} unidades"
        )
    else:
        producto_mas_vendido_label.config(text="No hay ventas registradas.")

    # Botón para cerrar la ventana
    cerrar_btn = Button(ventana_historial, text="Cerrar", command=ventana_historial.destroy)
    cerrar_btn.pack(pady=10)
    

# Registrar ventas para el historial
def registrar_venta():
    try:
        producto = producto_seleccionado.get()
        cantidad = int(cantidad_producto.get())

        # Buscar el producto en el inventario
        for item in inventario:
            if item["nombre"] == producto:
                if cantidad > item["cantidad"]:
                    resultado_label.config(text="Error: Productos insuficiente.")
                    return
                
                # Registrar la venta
                total = item["precio"] * cantidad
                historial_ventas.append({
                    "producto": producto,
                    "precio": item["precio"],
                    "cantidad": cantidad,
                    "total": total
                })

                # Actualizar el inventario
                item["cantidad"] -= cantidad
                resultado_label.config(text=f"Venta registrada: {cantidad} x {producto} (${total:.2f})")
                actualizar_menu()
                cantidad_producto.set("")  # Limpiar campo de cantidad
                return
        
        resultado_label.config(text="Error: Producto no encontrado.")
    except ValueError:
        resultado_label.config(text="Error: La cantidad debe ser un número entero.")
        
def calcular_producto_mas_vendido():
    if not historial_ventas:
        return {"producto": "Ninguno", "cantidad": 0}

    # Diccionario para almacenar las cantidades por producto
    cantidades = {}

    for venta in historial_ventas:
        producto = venta["producto"]
        cantidades[producto] = cantidades.get(producto, 0) + venta["cantidad"]

    # Encontrar el producto con mayor cantidad vendida
    producto_mas_vendido = max(cantidades, key=cantidades.get)
    return {"producto": producto_mas_vendido, "cantidad": cantidades[producto_mas_vendido]}



#agragar producto al inventario
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
        
        # limpiar datos anteriormente puestos
        nombre_producto.set('')
        precio_producto.set('')
        cantidad_producto.set('')
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
    resultado_label.configure(text=f"El producto se elimino.")

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
        
def modificar_producto():
    for producto in inventario:
        if producto["nombre"] == producto_seleccionado.get():
            try:
                nuevo_nombre = nombre_producto.get()
                nuevo_precio = precio_producto.get()
                nueva_cantidad = cantidad_producto.get()

                if nuevo_nombre:
                    producto["nombre"] = nuevo_nombre
                if nuevo_precio:
                    producto["precio"] = float(nuevo_precio)
                if nueva_cantidad:
                    producto["cantidad"] = int(nueva_cantidad)

                actualizar_menu()
                resultado_label.config(text=f"Producto '{producto['nombre']}' modificado con éxito.")
                return
            except ValueError as e:
                resultado_label.config(text=f"Error: {e}")
                return
    resultado_label.config(text="Error: Producto no encontrado.")


def ventas_productos():
    print('ventas totales')

############# BOTONES INTERACTIVOS Y LABES ############33   

# Widgets para agregar productos/ botones iteractivos

tituloLabel=Label(frame1, text='Ventas', fg='darkgreen', font=('Arial', 28))
tituloLabel.place(relx=.15, rely=.01, relheight=.15, relwidth=.70)

NombreLabel=Label(frame2, text="Nombre del Producto:", font=('Arial', 12))
NombreLabel.grid(row=0, column=0, padx=10, pady=10)
NombreEntrada=Entry(frame2, textvariable=nombre_producto)
NombreEntrada.grid(row=0, column=1, padx=10, pady=10)

PrecioLabel=Label(frame2, text="Precio del Producto:", font=('Arial', 12))
PrecioLabel.grid(row=1, column=0, padx=10, pady=10)
PrecioEntrada=Entry(frame2, textvariable=precio_producto)
PrecioEntrada.grid(row=1, column=1, padx=10, pady=10)

CantidadLabel=Label(frame2, text="Cantidad del Producto:", font=('Arial', 12))
CantidadLabel.grid(row=3, column=0, padx=10, pady=10)
CantidadEntrada=Entry(frame2, textvariable=cantidad_producto)
CantidadEntrada.grid(row=3, column=1,padx=10, pady=10)

# Widget para seleccionar un producto
SeleccioanarLabel=Label(frame2, text="Seleccionar Producto:", font=('Arial', 12))
SeleccioanarLabel.grid(row=1, column=7, columnspan=3)
opcion_menu = tk.OptionMenu(frame2, producto_seleccionado, "")
opcion_menu.config(bg='grey', width=12)
opcion_menu.place(x=350, y=100)

#boton para modificar el producto
modificarBoton=Button(frame1, text="Modificar", command=modificar_producto)
modificarBoton.place(relx=.25, rely=.25, relwidth=.5, relheight=.15)

agregarProductoBoton=Button(frame1, text="Agregar Producto", command=agregar_producto)
agregarProductoBoton.place(relx=.25, rely=.45, relwidth=.5, relheight=.15)


# Botones para acciones sobre productos
mostrarDetallesboton=Button(frame1, text="Mostrar Detalles", command=mostrar_detalles_producto)
mostrarDetallesboton.place(relx=.25, rely=.65, relwidth=.5, relheight=.15)

eliminarProductoBoton=Button(frame1, text="Eliminar Producto", command=eliminar_producto)
eliminarProductoBoton.place(relx=.25, rely=.85, relwidth=.5, relheight=.15)

#ventana de historial
HistorialBoton = Button(frame2, text="Historial de ventas", command=ventana_secundaria)
HistorialBoton.place(x=10, y=400)

#boton para registrar la venta
RegitrarBoton= Button(frame2, text='Registrar Venta', command=registrar_venta)
RegitrarBoton.place(x=300, y=400)


# Etiqueta para mostrar resultados o mensajes
resultado_label = Label(frame3, text="")
resultado_label.pack()



# Iniciar la aplicación
root.mainloop()

