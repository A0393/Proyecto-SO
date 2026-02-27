import time
import queue as q
import random
cola = []
cliente = 1
numero_clientes = random.randint(20,30)
dinero = random.randint(1000,2000)
for i in range (0,numero_clientes):
    cola += [cliente]
    cliente += 1
print(cola)
print(dinero)
cajero_1 = [random.randint(0,dinero-random.randint(0,dinero)), 0]
print (cajero_1)
cajero_2 = [random.randint(0,dinero-cajero_1[0]), 0]
print (cajero_2)
cajero_3 = [dinero-(cajero_2[0]+cajero_1[0]), 0]
print(cajero_3)