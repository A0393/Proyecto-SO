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
