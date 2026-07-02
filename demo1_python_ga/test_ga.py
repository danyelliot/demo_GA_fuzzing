"""
test_ga.py

Pruebas unitarias basicas que verifican que cada componente del AG
se comporta segun lo descrito en el paper (arXiv:2508.05923).

Ejecutar con:
    python -m unittest test_ga.py
"""

import unittest

from sut import run_sut, TOTAL_BRANCHES
from fitness import fitness, ramas_cubiertas
from population import generar_individuo, generar_poblacion_inicial
from selection import seleccion_por_torneo
from crossover import cruce_un_punto
from mutation import mutacion_reorder


class TestSUT(unittest.TestCase):
    def test_json_vacio_no_cubre_ninguna_rama(self):
        self.assertEqual(run_sut({}), [False, False, False, False])

    def test_json_completo_cubre_las_4_ramas(self):
        individuo = {"nombre": "A", "edad": 1, "activo": True, "rol": "user"}
        self.assertEqual(run_sut(individuo), [True, True, True, True])


class TestFitness(unittest.TestCase):
    def test_fitness_json_vacio_es_cero(self):
        self.assertEqual(fitness({}), 0.0)

    def test_fitness_json_completo_es_100(self):
        individuo = {"nombre": "A", "edad": 1, "activo": True, "rol": "user"}
        self.assertEqual(fitness(individuo), 100.0)

    def test_fitness_formula_coincide_con_ecuacion_1_del_paper(self):
        # Fitness(x) = B_exec(x) / B_total * 100
        individuo = {"nombre": "A", "edad": 1}  # cubre B1 y B2 -> 2 de 4
        esperado = (2 / TOTAL_BRANCHES) * 100
        self.assertEqual(fitness(individuo), esperado)

    def test_ramas_cubiertas_devuelve_nombres_correctos(self):
        individuo = {"activo": True}
        self.assertEqual(ramas_cubiertas(individuo), ["B3"])


class TestPoblacion(unittest.TestCase):
    def test_individuo_generado_es_subconjunto_de_campos_validos(self):
        individuo = generar_individuo()
        campos_validos = {"nombre", "edad", "activo", "rol"}
        self.assertTrue(set(individuo.keys()).issubset(campos_validos))
        self.assertGreaterEqual(len(individuo), 1)

    def test_poblacion_inicial_tiene_el_tamanio_solicitado(self):
        poblacion = generar_poblacion_inicial(10)
        self.assertEqual(len(poblacion), 10)


class TestSeleccion(unittest.TestCase):
    def test_torneo_siempre_elige_el_de_mayor_fitness_del_subconjunto(self):
        poblacion = [
            {"nombre": "A"},                                   # 25%
            {"nombre": "A", "edad": 1, "activo": True, "rol": "u"},  # 100%
        ]
        # con k = tamanio de poblacion completo, el torneo se reduce
        # a elegir siempre el maximo global
        ganador = seleccion_por_torneo(poblacion, k=len(poblacion))
        self.assertEqual(fitness(ganador), 100.0)


class TestCrossover(unittest.TestCase):
    def test_hijos_conservan_solo_genes_de_los_padres(self):
        padre1 = {"nombre": "A", "edad": 1}
        padre2 = {"activo": True, "rol": "user"}
        hijo1, hijo2 = cruce_un_punto(padre1, padre2)

        genes_padres = set(padre1.keys()) | set(padre2.keys())
        self.assertTrue(set(hijo1.keys()).issubset(genes_padres))
        self.assertTrue(set(hijo2.keys()).issubset(genes_padres))

    def test_padre_sin_genes_devuelve_copias_sin_error(self):
        hijo1, hijo2 = cruce_un_punto({}, {"nombre": "A"})
        self.assertEqual(hijo1, {})
        self.assertEqual(hijo2, {"nombre": "A"})


class TestMutacion(unittest.TestCase):
    def test_mutacion_no_cambia_el_contenido_solo_el_orden(self):
        individuo = {"nombre": "A", "edad": 1, "activo": True, "rol": "user"}
        mutado = mutacion_reorder(individuo)

        # mismo contenido (como conjuntos de items), sin importar el orden
        self.assertEqual(set(individuo.items()), set(mutado.items()))
        # el fitness no puede cambiar por reordenar: las claves son las mismas
        self.assertEqual(fitness(individuo), fitness(mutado))


if __name__ == "__main__":
    unittest.main()
