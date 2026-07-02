"""
population.py

Poblacion inicial (paper Sec. 3.1, Initial Input Generation).
El paper genera individuos desde una gramatica JSON formal, sin
seeds previos ("cold-start"). Aqui se usa una gramatica simplificada
acotada al SUT (sut.py).
"""

import random

# Genes posibles y su generador de valor (equivalente simplificado
# de las production rules de la gramatica del paper, Sec. 3.1).
CAMPOS_POSIBLES = {
    "nombre": lambda: random.choice(["Alice", "Bob", "Carla", "Diego"]),
    "edad":   lambda: random.randint(1, 99),
    "activo": lambda: random.choice([True, False]),
    "rol":    lambda: random.choice(["admin", "user", "guest"]),
}


def generar_individuo() -> dict:
    """Genera un individuo (JSON valido) con un subconjunto aleatorio de campos."""
    claves = list(CAMPOS_POSIBLES.keys())
    n_campos = random.randint(1, len(claves))
    claves_elegidas = random.sample(claves, n_campos)
    return {clave: CAMPOS_POSIBLES[clave]() for clave in claves_elegidas}


def generar_poblacion_inicial(tamanio: int) -> list:
    """
    Genera la poblacion inicial. El paper usa 100 individuos (Sec. 3.1);
    aqui es configurable y se usa un valor chico para poder leer el
    ciclo completo a mano.
    """
    return [generar_individuo() for _ in range(tamanio)]
