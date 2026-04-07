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
        self.lock = threading.Lock()

    def depositar(self, monto):
        with self.lock:
            temp = self.saldo
            time.sleep(0.1)
            temp += monto
            self.saldo = temp

    def retirar(self, monto):
        with self.lock:
            temp = self.saldo
            time.sleep(0.1)
            temp -= monto
            self.saldo = temp

# -----------------------
# Clase Cliente
# -----------------------
class Cliente:
    def __init__(self, id_cliente, tipo, monto):
        self.id = id_cliente
        self.tipo = tipo
        self.monto = monto
        self.memoria = random.randint(20, 100)

# -----------------------
# Función para escribir log
# -----------------------
def escribir_log(texto):
    with open("run.log", "a") as f:
        f.write(texto + "\n")

# -----------------------
# Función Cajero (Hilo)
# -----------------------
def cajero(id_cajero, banco, cola):
    while not cola.empty():
        cliente = cola.get()

        print(f"[Cajero {id_cajero}] INICIA Cliente {cliente.id} - Memoria: {cliente.memoria}MB")
        time.sleep(1)
        print(f"[Cajero {id_cajero}] TERMINA Cliente {cliente.id}")

        if cliente.tipo == "deposito":
            banco.depositar(cliente.monto)
        else:
            banco.retirar(cliente.monto)

        log = f"Cajero {id_cajero} atendió Cliente {cliente.id} - {cliente.tipo} ${cliente.monto} - Memoria: {cliente.memoria}MB"
        print(log)
        escribir_log(log)

        cola.task_done()

# -----------------------
# Programa principal
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
        cliente = Cliente(i + 1, tipo, monto)
        cola_clientes.put(cliente)

    print(f"Saldo actual: {banco.saldo}")
    print(f"Clientes en espera: {cola_clientes.qsize()}")
    print("Cajeros activos: 3\n")

    # Crear 3 cajeros
    hilos = []
    for i in range(3):
        t = threading.Thread(target=cajero, args=(i + 1, banco, cola_clientes))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print("\nSaldo final:", banco.saldo)
