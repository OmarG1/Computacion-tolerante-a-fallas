import pickle

'''
Alumno: Gomez Quintero Omar Federico

Generar un programa que sea capaz de restaurar el estado de ejecución. 

Se creo una clase con la cual se crearon objetos con asignacion de valores a sus atributos, en este caso se crearon dos y se guardaron en un diccionario
una vez guardados en el diccionario utilizando pickle se guardaron los datos en un archivo llamado estado_programa.pkl, se muestran los datos que se guardaron y
despues se borraron todos los datos, tanto los objetos como el diccionario, utilizando el metodo para obtener los valores del archivo le asignamos de nuevo
los valores al diccionario llamado componentes una vez restaurados los valores en este se volvieron a imprimir en pantalla mostrando la correcta restauracion
'''

# Clase a utilizar
class Tecnologia:
    def __init__(self):
        self.nombre = ""
        self.costo = 0
        self.cantidad = 0

# Variables y instanciacion de objetos
componentes = {}

computadora = Tecnologia()
computadora.nombre = "computadora"
computadora.costo = 25000
computadora.cantidad = 10
componentes[computadora.nombre] = computadora

teclado = Tecnologia()
teclado.nombre = "teclado"
teclado.costo = 1500
teclado.cantidad = 4
componentes[teclado.nombre] = teclado

# Guardado de los datos en el diccionario en el archivo 
with open("estado_programa.pkl","wb") as file:
    pickle.dump(componentes,file)

# Muestra los valores guardados
for nombre, componente in componentes.items():
    print(f"Estado actual guardado Nombre: {nombre}, Costo: {componente.costo}, Cantidad: {componente.cantidad}")

# Se borran los valores
del computadora
del teclado
del componentes

# Se recuperan los datos del archivo y se asignan al diccionario
with open("estado_programa.pkl","rb") as file:
    componentes = pickle.load(file)

print("")

# Se muestran los valores restaurados
for nombre, componente in componentes.items():
    print(f"Estado restaurado Nombre: {nombre}, Costo: {componente.costo}, Cantidad: {componente.cantidad}")

