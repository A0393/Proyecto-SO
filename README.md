# Proyecto-SO
Simulador de Banco con Cajeros Concurrentes

Camila Hurtado Murillo
Octavio Jimenez
Alejandro Aguirre

# Como ejecutar

Tener python 3 instalado.
Ejecutar: 
1. main.py

# Descripción: El sistema simula clientes que realizan depósitos y retiros.
Tres cajeros atienden clientes desde una cola compartida.

# Propuesta Técnica

# Problema
Simular el funcionamiento de un banco donde múltiples cajeros atienden clientes de manera concurrente. El sistema permitirá observar como varios hilos acceden a recursos compartidos, generando posibles condiciones de carrera que luego serán solucionadas mediante mecanismos de sincronización.

# Objetivo General
Desarrollar una aplicación en Python que modele la atención de clientes en un banco usando hilos reales, una cola compartida y un saldo global del banco.

# Arquitectura General
El sistema estará compuesto por los siguientes módulos:
1. Cliente: Representa una operación (depósito o retiro)
2. Cajero: Atiende clientes de forma concurrente
3. Banco: Mantiene el saldo global compartido
4. Cola de clientes: Estructura FIFO compartida entre hilos

# Tecnologías
Lenguaje: Python
Librerías: threading, queue, time

# Funcionamiento Básico
1. Se generan varios clientes con operaciones aleatorias
2. Los clientes se agregan en una cola compartida
3. Tres cajeros atienden clientes simultáneamente
4. Cada cajero modifica e saldo global
5. En futuras entregas se implementará sincornización con Lock

# MOCK / BOCETO

--------------------------------------------
BANCO
--------------------------------------------

Saldo actual: 1000
Clientes en espera: 5
Cajeros activos: 3

[Cajero 1] Atendiendo Cliente 3 - Retiro $200
[Cajero 2] Atendiendo Cliente 4 - Déposito $150
[Cajero 3] Atendiendo Cliente 5 - Retiro $100

Saldo actual: $850


