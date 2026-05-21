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
            saldo_anterior = self.saldo
            time.sleep(0.2)

            self.saldo += monto

            print(
                f"DEPOSITO | Antes: {saldo_anterior} "
                f"Ahora: {self.saldo}"
            )

    def retirar(self, monto):
        with self.lock:
            saldo_anterior = self.saldo

            if self.saldo >= monto:
                time.sleep(0.2)

                self.saldo -= monto

                print(
                    f"RETIRO | Antes: {saldo_anterior} "
                    f"Ahora: {self.saldo}"
                )

                return True

            print(
                f"RECHAZADO | "
                f"Saldo insuficiente: {self.saldo}"
            )

            return False


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

    print(f"SO         : {platform.system()} {platform.release()}")
    print(f"Versión    : {platform.version()[:50]}")
    print(f"Máquina    : {platform.machine()}")
    print(f"Procesador : {platform.processor()[:40] or 'N/A'}")

    cpu_logico = psutil.cpu_count(logical=True)
    cpu_fisico = psutil.cpu_count(logical=False)
    cpu_uso = psutil.cpu_percent(interval=0.5)

    print(f"\nCPUs       : {cpu_fisico} físicos / {cpu_logico} lógicos")
    print(f"Uso CPU    : {cpu_uso:.1f}%")

    mem = psutil.virtual_memory()

    print(f"\nRAM total  : {mem.total / (1024**3):.2f} GB")
    print(f"RAM usada  : {mem.used / (1024**3):.2f} GB")
    print(f"RAM libre  : {mem.available / (1024**3):.2f} GB")

    proc = psutil.Process(os.getpid())
    mem_proc = proc.memory_info()

    print(f"\nPID actual : {os.getpid()}")
    print(f"RAM proceso: {mem_proc.rss / (1024**2):.2f} MB")
    print(f"Threads    : {proc.num_threads()}")

    print("=" * 50)
    print()


# -----------------------
# Captura de recursos
# -----------------------
def capturar_recursos_hilo():
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info()

    return {
        "rss_mb": mem.rss / (1024**2),
        "hilos": threading.active_count()
    }


# -----------------------
# Escribir log
# -----------------------
def escribir_log(texto):
    with open("run.log", "a", encoding="utf-8") as f:
        f.write(texto + "\n")


# -----------------------
# Función Cajero
# -----------------------
def cajero(id_cajero, banco, cola, resultados):

    atendidos = 0
    recursos_pico = {"rss_mb": 0.0}

    while True:

        try:
            cliente = cola.get_nowait()

        except queue.Empty:
            break

        antes = capturar_recursos_hilo()

        print(
            f"[Cajero {id_cajero}] INICIA Cliente {cliente.id} "
            f"| RAM: {antes['rss_mb']:.1f} MB "
            f"| Hilos: {antes['hilos']}"
        )

        time.sleep(1)

        if cliente.tipo == "deposito":

            banco.depositar(cliente.monto)

            resultado = f"depósito +${cliente.monto}"

        else:

            ok = banco.retirar(cliente.monto)

            if ok:
                resultado = f"retiro -${cliente.monto}"
            else:
                resultado = "RECHAZADO"

        despues = capturar_recursos_hilo()

        if despues["rss_mb"] > recursos_pico["rss_mb"]:
            recursos_pico["rss_mb"] = despues["rss_mb"]

        log = (
            f"Cajero {id_cajero} atendió Cliente {cliente.id} "
            f"- {cliente.tipo} ${cliente.monto} "
            f"- Memoria cliente: {cliente.memoria}MB"
        )

        print(f"[Cajero {id_cajero}] TERMINA Cliente {cliente.id}")

        escribir_log(log)

        atendidos += 1

        cola.task_done()

    resultados[id_cajero] = {
        "atendidos": atendidos,
        "ram_pico_mb": recursos_pico["rss_mb"]
    }


# -----------------------
# Programa principal
# -----------------------
if __name__ == "__main__":

    inicio_total = time.time()

    print("--------------------------------------------")
    print("BANCO")
    print("--------------------------------------------")

    # Limpiar log viejo
    if os.path.exists("run.log"):
        os.remove("run.log")

    mostrar_info_sistema()

    banco = Banco(1000)

    cola_clientes = queue.Queue()

    # Crear clientes
    for i in range(5):

        tipo = random.choice(["deposito", "retiro"])
        monto = random.randint(50, 300)

        cliente = Cliente(i + 1, tipo, monto)

        cola_clientes.put(cliente)

    print(f"Saldo inicial: {banco.saldo}")
    print(f"Clientes en espera: {cola_clientes.qsize()}")
    print("Cajeros activos: 3\n")

    # Crear cajeros
    resultados = {}
    hilos = []

    for i in range(3):

        t = threading.Thread(
            target=cajero,
            args=(i + 1, banco, cola_clientes, resultados)
        )

        hilos.append(t)

        t.start()

    # Esperar hilos
    for t in hilos:
        t.join()

    fin_total = time.time()

    # -----------------------
    # Estadísticas
    # -----------------------
    print("\n===== ESTADÍSTICAS =====")

    print(f"Tiempo total: {fin_total - inicio_total:.2f}s")

    print(f"Saldo final: {banco.saldo}")

    print("Clientes procesados: 5")

    print("Hilos utilizados: 3")

    escribir_log(
        f"Tiempo total: {fin_total - inicio_total:.2f}s"
    )

    escribir_log(
        f"Saldo final: {banco.saldo}"
    )
