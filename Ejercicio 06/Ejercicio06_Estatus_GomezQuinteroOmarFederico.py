# Gomez Quintero Omar Federico

import tkinter as tk
from tkinter import *
from tkinter import END,messagebox
import psutil

root=tk.Tk()
root.title("Administrador")
root.config(width=300,height=300)

# Procesos
lb_tituloProceso=Label(root,text="Proceso")
lb_tituloProceso.place(x=30,y=10)
lb_tituloProceso.config(font=("Arial",12))

lb_tituloEstatus=Label(root,text="Estatus")
lb_tituloEstatus.place(x=180,y=10)
lb_tituloEstatus.config(font=("Arial",12))

lb_proceso1=Label(root,text="Brave Browser")
lb_proceso1.place(x=15,y=40)
lb_proceso1.config(font=("Arial",10))

lb_proceso2=Label(root,text="Calculadora OB")
lb_proceso2.place(x=15,y=70)
lb_proceso2.config(font=("Arial",10))

lb_proceso3=Label(root,text="Pixelorama")
lb_proceso3.place(x=15,y=100)
lb_proceso3.config(font=("Arial",10))

# Estado de los procesos
lb_estado1=Label(root,text="----")
lb_estado1.place(x=185,y=40)
lb_estado1.config(font=("Arial",10))

lb_estad2=Label(root,text="----")
lb_estad2.place(x=185,y=70)
lb_estad2.config(font=("Arial",10))

lb_estad3=Label(root,text="----")
lb_estad3.place(x=185,y=100)
lb_estad3.config(font=("Arial",10))

# Funcion para actualizar el estado de los procesos

estadoInicialBrave=False
estadoInicialCalculadora=False
estadoInicialPixelorama=False

def actualizar_estado():
    global estadoInicialBrave, estadoInicialCalculadora,estadoInicialPixelorama
    encontradoBrave=False
    encontradoCalculadora=False
    encontradoPixelorama=False
    for proceso in psutil.process_iter():
        try:
            if "brave" in proceso.name().lower():
                lb_estado1.config(text="Activo")
                encontradoBrave=True
                estadoInicialBrave=True
            if "app.exe" == proceso.name().lower():
                lb_estad2.config(text="Activo")
                encontradoCalculadora=True
                estadoInicialCalculadora=True
            if "pixelorama" in proceso.name().lower():
                lb_estad3.config(text="Activo")
                encontradoPixelorama=True
                estadoInicialPixelorama=True

        except(Exception):
            pass
    
    if encontradoBrave==False:
        if estadoInicialBrave == False:
            lb_estado1.config(text="Sin detectar")
        else:
            lb_estado1.config(text="Detenido")
    if encontradoCalculadora == False:
        if estadoInicialCalculadora == False:
            lb_estad2.config(text="Sin detectar")
        else:
            lb_estad2.config(text="Detenido")
    if encontradoPixelorama == False:
        if estadoInicialPixelorama == False:
            lb_estad3.config(text="Sin detectar")
        else:
            lb_estad3.config(text="Detenido")
    
    estadoInicialBrave = encontradoBrave
    estadoInicialCalculadora = encontradoCalculadora
    estadoInicialPixelorama = encontradoPixelorama
    root.after(1000,actualizar_estado)


actualizar_estado()

root.mainloop()