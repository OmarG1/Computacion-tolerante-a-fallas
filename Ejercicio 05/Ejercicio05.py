# Alumno: Gomez Quintero Omar Federico

# Uso de hilos, procesos, demonios y concurrencia
# Se crearon hilos para la concurrencia, uno de estos guarda productos en una lista y otro muestra todos los productos, se creo un proceso para que realice la busqueda de algun dato en la lista
# Para que se compartan los datos entre los procesos se utiliza manager  y queue

import tkinter as tk
import threading
import multiprocessing
import time


def hilo_mostrar(name, listbox, productos):
    print(f"Hilo ejecutando: {name}")
    listbox.delete(0, tk.END)
    for producto in productos:
        listbox.insert(tk.END, producto)
    time.sleep(2)
    print(f"Hilo terminado: {name}")

def hilo_guardar(nombre, dato, productos):
    print(f"Hilo ejecutando: {nombre}")
    productos.append(dato)
    time.sleep(2)
    print(f"Hilo terminado: {nombre}")

def proceso_buscar(nombre, productos, resultado):
    print(f"Proceso de busqueda ejecutando: {nombre}")
    for producto in productos:
        if producto == nombre:
            resultado.put(f"Producto '{nombre}' encontrado")
            break
        else:
            resultado.put(f"Producto '{nombre}' no encontrado")
    time.sleep(2)
    print(f"Proceso de busqueda terminado: {nombre}")

def iniciar_hilo_mostrar(listbox, productos):
    hilo = threading.Thread(target=hilo_mostrar, args=("Mostrar", listbox, productos))
    hilo.daemon = True
    hilo.start()

def iniciar_hilo_guardar(display, productos):
    producto_txt = display.get()
    hilo = threading.Thread(target=hilo_guardar, args=("Guardar", producto_txt, productos))
    hilo.daemon = True
    hilo.start()

def iniciar_proceso_buscar(display, productos, resultado):
    producto_txt = display.get()
    proceso = multiprocessing.Process(target=proceso_buscar, args=(producto_txt, productos, resultado))
    proceso.start()

if __name__ == "__main__":
    productos = ["Teclado","Monitor"]

    # Interfaz
    root = tk.Tk()
    root.title("Procesos y hilos")
    root.config(width=400, height=300)

    txt_display_guardar = tk.Entry(root)
    txt_display_guardar.place(x=10, y=20)

    listbox = tk.Listbox(root)
    listbox.place(x=10, y=100, width=200, height=180)

    btnGuardar = tk.Button(root, text="Guardar", command=lambda: iniciar_hilo_guardar(txt_display_guardar, productos_proxy))
    btnGuardar.place(x=140, y=16)

    btnMostrar = tk.Button(root, text="Mostrar productos", command=lambda: iniciar_hilo_mostrar(listbox, productos_proxy))
    btnMostrar.place(x=50, y=70)

    # Permite la comunicacion entre procesos de la lista y por medio de la cola
    manager = multiprocessing.Manager()
    productos_proxy = manager.list(productos)
    resultado = multiprocessing.Queue()
    btnBuscar = tk.Button(root, text="Buscar", command=lambda: iniciar_proceso_buscar(txt_display_guardar, productos_proxy, resultado))
    btnBuscar.place(x=196, y=16)

    lblResultado = tk.Label(root, text="")
    lblResultado.place(x=125, y=50)

    # Actualiza cada sierto tiempo el resultado a mostrar
    def actualizar_resultado():
        if not resultado.empty():
            resultado_str = resultado.get()
            lblResultado.config(text=resultado_str)
        root.after(100, actualizar_resultado)

    actualizar_resultado()

    root.mainloop()