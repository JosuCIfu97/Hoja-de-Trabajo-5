# -*- coding: cp1252 -*-
#Universidad del Valle de Guatemala
#Algoritmos y Estructuras de Datos
#Sección 20
#Josué Cifuentes 15275
#Pablo Muñoz 15258
#30/08/16
#Hoja de Trabajo No. 5
#El código se basó en los ejemplos de clase y de blackboard

import simpy
import random

#Método de simulación
#env: environment de simpy
#name: nombre del proceso:
#time: tiempo que toma cada "event"
#ram: Memoria en uso
#memory: Capacidad máxima de memoria
#instructions: Número de instrucciones por el proceso.
#speed: velocidad del procesador (instrucciones/unidad de tiempo)
def proceso(env, name, time, ram, memory, instructions, speed):
    global times

    #New: Proceso llega al SO esperando que se le asigne memoria RAM.
    yield env.timeout(time) #Se debe esperar la llegada del proceso
    arrival = env.now #Guarda tiempo de llegada
    print ('tiempo %f : %s (NEW) solicita %d de memoria ram' % (arrival, name, memory))
    
    #Ready: Proceso listo para correr para cuando se desocupe CPU.
    yield ram.get(memory) #Espera a que haya espacio disponible en la ram
    print ('tiempo %f : %s (ADMITTED) solicitud aceptada por %d de memoria ram' % (env.now, name, memory))

    #Almacenamiento de instrucciones terminadas.
    completed = 0
    while completed < instructions: #Deben haber instrucciones sin terminar para trabajar con el proceso
        #Conexión con CPU
        with cpu.request() as r:
            yield r #Espera al que el Resource del CPU esté disponible
            if speed <= (instructions - completed):
                running = speed #El máximo de instrucciones que pueden ejecutarse depende de la velocidad del procesador (3 en este caso).
            else:
                running = instructions - completed

            print ('tiempo %f : %s (READY) se ejecutarán %d instrucciones' % (env.now, name, running))
            yield env.timeout(running/speed) #máximo 1 unidad de tiempo para realizar las instrucciones.
            completed += running #Ya ejecutó las instrucciones el CPU.
            print ('tiempo %f: %s (RUNNING) instrucciones (%d/%d) completadas.' % (env.now, name, completed, instructions))

            #Decisión del procesador si poner demás instrucciones en espera o listas.
            decision = random.randint(1,2)
            if decision ==1 and completed < instructions: #Ya se ejecutaron nuevas instrucciones por lo que debe valuarse que no se hayan completado todas ya.
                with wait.request() as w:
                    yield w
                    
                    print ('tiempo %f : %s (WAITING) operaciones I/O finalizadas' % (env.now, name))

    #Terminated: Proceso ya finalizado
    yield ram.put(memory) #Se libera memoria ocupada por proceso.
    print ('tiempo %f : %s (TERMINATED) libera %d de memoria ram' % (env.now, name, memory))
    #Se guarda en la lista el tiempo total del proceso
    terminated = env.now
    times.append(terminated-arrival)

#VARIABLES
speed = 3.0 #instrucciones/unidad de tiempo
total_memory = 100 #Cantidad total (máxima) de memoria ram disponible.
processes = 25 #Procesos totales a ejecutar
times = [] #Lista que contendrá todos los tiempos
interval = 1

env = simpy.Environment()
cpu = simpy.Resource (env, capacity=2)
ram = simpy.Container(env, init=total_memory, capacity=total_memory)
wait = simpy.Resource(env, capacity=2)

#Random
random.seed(2048)

for i in range(processes):
    time = random.expovariate(1.0/interval)
    instructions = random.randint(1,10)
    memory = random.randint(1,10)
    env.process(proceso(env, 'Proceso %d' % (i+1), time, ram, memory, instructions, speed))
    
env.run()

#Tiempo total y desviación estándar
sumatoria = 0
for i in times:
    sumatoria = sumatoria + i
prom = sumatoria/processes

sumdesv = 0
for x in times:
    sumdesv = sumdesv + (x-prom)**2
s = (sumdesv/(processes-1))**0.5

print ""
print ('El tiempo promedio es %f' %(prom))
print ("La desviació estándar es %f" % (s))

            
