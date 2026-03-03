import threading
import queue
import random
import time

# -----------------------
# Clase Banco
# -----------------------
class Banco:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        self.saldo -= monto

# -----------------------
# Clase Cliente
# -----------------------
class Cliente:
    def __init__(self, id_cliente, tipo, monto):
        self.id = id_cliente
        self.tipo = tipo
        self.monto = monto

# -----------------------
# Programa principal (Commit 1)
# -----------------------
if __name__ == "__main__":

    print("--------------------------------------------")
    print("BANCO")
    print("--------------------------------------------")

    banco = Banco(1000)
    cola_clientes = queue.Queue()

    # Generar 5 clientes aleatorios
    for i in range(5):
        tipo = random.choice(["deposito", "retiro"])
        monto = random.randint(50, 300)
        cliente = Cliente(i+1, tipo, monto)
        cola_clientes.put(cliente)

    print(f"Saldo actual: {banco.saldo}")
    print(f"Clientes en espera: {cola_clientes.qsize()}")
    
    print("Cajeros activos: 3\n")

# -----------------------
# Función Cajero (Hilo)
# -----------------------
def cajero(id_cajero, banco, cola):
    while not cola.empty():
        cliente = cola.get()

        print(f"[Cajero {id_cajero}] Atendiendo Cliente {cliente.id} - {cliente.tipo} ${cliente.monto}")

        time.sleep(1)  # Simula tiempo de atención

        if cliente.tipo == "deposito":
            banco.depositar(cliente.monto)
        else:
            banco.retirar(cliente.monto)

        cola.task_done()

# Crear 3 cajeros
hilos = []
for i in range(3):
    t = threading.Thread(target=cajero, args=(i+1, banco, cola_clientes))
    hilos.append(t)
    t.start()

for t in hilos:
    t.join()

print("\nSaldo actual:", banco.saldo)
