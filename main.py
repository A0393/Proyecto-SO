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
