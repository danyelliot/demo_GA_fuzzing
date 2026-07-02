"""
sut.py

SUT de ejemplo: parser JSON con 4 ramas de decision. Programa
objetivo sobre el que el AG maximiza branch coverage (paper Sec. 3.3,
arXiv:2508.05923).

La cobertura se registra a mano; en un caso real (AFL++, ver
demo2_afl_fuzzing/) la mide la instrumentacion del binario.
"""

TOTAL_BRANCHES = 4  # B_total, Ecuacion 1 (Sec. 3.3)

NOMBRES_RAMAS = ["B1", "B2", "B3", "B4"]


def run_sut(individuo: dict) -> list:
    """
    Ejecuta el SUT sobre un individuo y devuelve que ramas cubre:
        B1 -> tiene clave "nombre"
        B2 -> tiene clave "edad"
        B3 -> tiene clave "activo"
        B4 -> tiene clave "rol"
    """
    cubiertas = [False, False, False, False]

    if "nombre" in individuo:       # rama B1
        cubiertas[0] = True
        _ = individuo["nombre"]

    if "edad" in individuo:         # rama B2
        cubiertas[1] = True
        _ = individuo["edad"]

    if "activo" in individuo:       # rama B3
        cubiertas[2] = True
        _ = individuo["activo"]

    if "rol" in individuo:          # rama B4
        cubiertas[3] = True
        _ = individuo["rol"]

    return cubiertas
