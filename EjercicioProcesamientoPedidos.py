import threading
import time
import random
import queue


colaPedidos = queue.Queue(maxsize=5)  #Cola compartida con capacidad 5
pedidosGenerados = 0  #Contador de pedidos generados
lock = threading.Lock()  #Bloquo para gestionar el acceso al contador de pedidos


def cliente(idCliente):
    global pedidosGenerados
    while True:
        #Bloqueamos el acceso a pedidosGenerados para evitar condiciones de carrera
        with lock:
            #Salimos del bucle si ya se han generado todos los pedidos
            if pedidosGenerados >= 15:
                break
            pedidosGenerados += 1 #Incrementamos el contador de pedidos generados
            numPedidoActual = pedidosGenerados #Guardamos el número del pedido actual

        #Creamos un pedido y lo añadimos a la cola
        pedido = f"Pedido-{numPedidoActual}"
        colaPedidos.put(pedido)
        print(f"Cliente {idCliente}: Generó {pedido}")
        time.sleep(random.uniform(1, 2))  #Simulamos el tiempo de generación


def empleado(idEmpleado):
    while True:
        # Bloqueamos el acceso a pedidosGenerados para verificar el contador de pedidos
        with lock:
            #Salimos del bucle si la cola está vacía y ya no quedan pedidos por generar
            if colaPedidos.empty() and pedidosGenerados >= 15:
                break

        #Obtenemos un pedido de la cola
        pedido = colaPedidos.get()  # Espera un pedido de la cola
        print(f"Empleado {idEmpleado}: Procesó {pedido}")
        time.sleep(random.uniform(2, 3))  #Simulamos el tiempo de procesamiento
        colaPedidos.task_done() #Indica que el pedido ha sido procesado

#Creamos listas para almacenar los hilos de clientes y empleados
clientes = []
empleados = []

#Creamos e iniciamos los hilos para los clientes
for i in range(1, 4):
    t = threading.Thread(target=cliente, args=(i,))
    clientes.append(t)
    t.start()

#Creamos e iniciamos los hilos para los empleados
for i in range(1, 3):
    t = threading.Thread(target=empleado, args=(i,))
    clientes.append(t)
    t.start()

#Esperamos a que todos los hilos terminen
for cliente in clientes:
    cliente.join()

for empleado in empleados:
    empleado.join()

print("Todos los pedidos han sido procesados.")
