import threading
import queue
import random
import time
import os
import psutil
import platform

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
# Información del sistema
# -----------------------

def mostrar_info_sistema():
    print("=" * 50)
    print("  INFORMACIÓN DEL SISTEMA")
    print("=" * 50)
 
    # Sistema operativo
    print(f"  SO         : {platform.system()} {platform.release()}")
    print(f"  Versión    : {platform.version()[:50]}")
    print(f"  Máquina    : {platform.machine()}")
    print(f"  Procesador : {platform.processor()[:40] or 'N/A'}")
 
    # CPU
    cpu_count_logico = psutil.cpu_count(logical=True)
    cpu_count_fisico = psutil.cpu_count(logical=False)
    cpu_uso = psutil.cpu_percent(interval=0.5)
    print(f"\n  CPUs       : {cpu_count_fisico} físicos / {cpu_count_logico} lógicos")
    print(f"  Uso CPU    : {cpu_uso:.1f}%")
 
    # Memoria RAM
    mem = psutil.virtual_memory()
    print(f"\n  RAM total  : {mem.total / (1024**3):.2f} GB")
    print(f"  RAM usada  : {mem.used  / (1024**3):.2f} GB ({mem.percent:.1f}%)")
    print(f"  RAM libre  : {mem.available / (1024**3):.2f} GB")
 
    # Proceso actual
    proc = psutil.Process(os.getpid())
    mem_proc = proc.memory_info()
    print(f"\n  PID actual : {os.getpid()}")
    print(f"  RAM proceso: {mem_proc.rss / (1024**2):.2f} MB (RSS)")
    print(f"  Threads    : {proc.num_threads()}")
    print("=" * 50)
    print()

def capturar_recursos_hilo(id_cajero):
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info()
    cpu = proc.cpu_percent(interval=None)
    hilos_activos = threading.active_count()
    return {
        "rss_mb":  mem.rss  / (1024**2),
        "vms_mb":  mem.vms  / (1024**2),
        "cpu_pct": cpu,
        "hilos":   hilos_activos,
    }

# -----------------------
# Función para escribir log
# -----------------------
def escribir_log(texto):
    with open("run.log", "a") as f:
        f.write(texto + "\n")

# -----------------------
# Función Cajero (Hilo)
# -----------------------
def cajero(id_cajero, banco, cola, resultados):
    atendidos = 0
    recursos_pico = {"rss_mb": 0.0}
    while not cola.empty():
        try:
            cliente = cola.get_nowait()
        except queue.Empty:
            break

        antes = capturar_recursos_hilo(id_cajero)
 
        print(f"  [Cajero {id_cajero}] INICIA  Cliente {cliente.id:<2} "
              f"| RAM proceso: {antes['rss_mb']:.1f} MB "
              f"| Hilos activos: {antes['hilos']}")
        time.sleep(1)

        if cliente.tipo == "deposito":
            banco.depositar(cliente.monto)
            resultado = f"depósito  +${cliente.monto}"
        else:
           ok = banco.retirar(cliente.monto)
           resultado = f"retiro    -${cliente.monto}" if ok else f"RECHAZADO (fondos insuficientes)"

        despues = capturar_recursos_hilo(id_cajero)
 
        if despues["rss_mb"] > recursos_pico["rss_mb"]:
            recursos_pico["rss_mb"] = despues["rss_mb"]
 
        log = (f"Cajero {id_cajero} | Cliente {cliente.id} | {resultado} "
               f"| RAM antes: {antes['rss_mb']:.1f} MB  después: {despues['rss_mb']:.1f} MB ")
        
        print(f"[Cajero {id_cajero}] TERMINA Cliente {cliente.id}")

        log = f"Cajero {id_cajero} atendió Cliente {cliente.id} - {cliente.tipo} ${cliente.monto} - Memoria: {cliente.memoria}MB"
        print(log)
        atendidos += 1
        escribir_log(log)
    cola.task_done()
    resultados[id_cajero] = {"atendidos": atendidos, "ram_pico_mb": recursos_pico["rss_mb"]}


# -----------------------
# Programa principal
# -----------------------
if __name__ == "__main__":

    print("--------------------------------------------")
    print("BANCO")
    print("--------------------------------------------")

    if os.path.exists("run.log"):
        os.remove("run.log")

    mostrar_info_sistema()

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
    resultados = {}
    hilos = []
    for i in range(3):
        t = threading.Thread(target=cajero, args=(i + 1, banco, cola_clientes, resultados))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print("\nSaldo final:", banco.saldo)
