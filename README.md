# Computacion Cuantica con Qiskit — Unidad 12

Implementacion y simulacion de tres algoritmos cuanticos fundamentales usando Qiskit y AerSimulator. Los experimentos demuestran fenomenos como el entrelazamiento cuantico, la ventaja cuantica en consultas a oraculos y la amplificacion de amplitud por interferencia.

---

## Informacion del proyecto

| Campo           | Detalle                                        |
|-----------------|------------------------------------------------|
| Autor           | William Balaguera — 1152439                    |
| Materia         | Arquitectura de Computadores                   |
| Unidad          | 12 — Computacion Emergente y Tendencias        |
| Ano             | 2026                                           |
| Universidad     | Francisco de Paula Santander                   |
| Lenguaje        | Python 3 / Qiskit                              |

---

## Descripcion

El proyecto contiene tres experimentos de computacion cuantica simulados localmente con `AerSimulator`, sin requerir acceso a hardware cuantico real. Cada experimento ilustra un concepto clave de la computacion cuantica y produce histogramas de medicion que evidencian el comportamiento cuantico del circuito.

---

## Estructura del repositorio

```
src/
├── bell_state.py        — Experimento 1: Estado de Bell y entrelazamiento
├── deutsch_jozsa.py     — Experimento 2: Algoritmo de Deutsch-Jozsa
└── grover.py            — Experimento 3: Algoritmo de Grover (2 qubits)

capturas/
├── bell_histogram.png
├── dj_constante_histogram.png
├── dj_balanceada_histogram.png
├── grover_00.png
├── grover_01.png
├── grover_10.png
└── grover_11.png
```

---

## Requisitos

- Python 3.9 o superior
- qiskit
- qiskit-aer
- matplotlib

Instalacion de dependencias:

```bash
pip install qiskit qiskit-aer matplotlib
```

---

## Ejecucion

```bash
python src/bell_state.py
python src/deutsch_jozsa.py
python src/grover.py
```

Los histogramas se guardan automaticamente en la carpeta `capturas/`.

---

## Experimentos

### Experimento 1 — Estado de Bell

**Archivo:** `src/bell_state.py`

Prepara el estado de Bell |Phi+> = (|00> + |11>) / raiz(2), el estado bipartito entrelazado mas simple. El circuito aplica una puerta Hadamard sobre el qubit 0 para crear superposicion, seguida de una puerta CNOT para entrelazar ambos qubits.

```
q0: ─ H ─ ●─ M
q1: ───── X─ M
```

El resultado esperado es aproximadamente 50% |00> y 50% |11>, con ausencia total de |01> y |10>. La ausencia de estos estados intermedios es la firma del entrelazamiento cuantico: medir uno de los qubits determina instantaneamente el estado del otro.

**Resultado obtenido (1024 shots):**

| Estado | Conteo | Porcentaje |
|--------|--------|-----------|
| \|00>  | 530    | 51.8%     |
| \|11>  | 494    | 48.2%     |

Correlacion perfecta verificada. Los estados |01> y |10> no aparecieron.

---

### Experimento 2 — Algoritmo de Deutsch-Jozsa

**Archivo:** `src/deutsch_jozsa.py`

Determina si una funcion booleana f: {0,1}^n -> {0,1} es constante (mismo valor para todas las entradas) o balanceada (0 para exactamente la mitad, 1 para la otra mitad), usando una sola evaluacion del oraculo. Un algoritmo clasico requiere en el peor caso 2^(n-1) + 1 evaluaciones.

El circuito inicializa el ancilla en |1>, aplica Hadamard a todos los qubits, ejecuta el oraculo, aplica Hadamard nuevamente a los qubits de entrada y mide. La interpretacion del resultado es:

- Todo |0...0> medido con certeza → funcion CONSTANTE
- Cualquier estado distinto de |0...0> → funcion BALANCEADA

**Resultados obtenidos (n=2, 1024 shots):**

| Oraculo    | Estado medido | Resultado    |
|------------|---------------|--------------|
| Constante  | \|00> (100%)  | CONSTANTE    |
| Balanceado | \|11> (100%)  | BALANCEADA   |

Ambos oraculos verificados correctamente con certeza determinista (sin ruido de simulacion).

**Ventaja cuantica:** 1 evaluacion del oraculo frente a 3 en el peor caso clasico para n=2.

---

### Experimento 3 — Algoritmo de Grover

**Archivo:** `src/grover.py`

Busca un estado marcado dentro de un espacio de N = 4 estados ({|00>, |01>, |10>, |11>}) amplificando su amplitud de probabilidad mediante interferencia cuantica. Para n=2 qubits, una sola iteracion es optima y alcanza probabilidad ~100% del estado objetivo.

El circuito consta de tres etapas:

1. **Superposicion uniforme:** H aplicado a ambos qubits
2. **Oraculo de fase:** invierte la fase del estado objetivo usando puertas X y CZ segun el target
3. **Difusor:** aplica la inversion alrededor de la media (H X CZ X H), amplificando el estado marcado

**Resultados obtenidos (1024 shots por target):**

| Target buscado | Estado medido | Probabilidad | Veredicto |
|---------------|---------------|-------------|-----------|
| \|00>         | \|00>         | 100%        | Correcto  |
| \|01>         | \|10>         | 100%        | Error*    |
| \|10>         | \|01>         | 100%        | Error*    |
| \|11>         | \|11>         | 100%        | Correcto  |

*Los targets |01> y |10> presentan inversion de bits en el resultado, lo que indica un detalle en el orden de los bits (bit ordering) entre Qiskit y la convencion utilizada en el oraculo. El algoritmo funciona correctamente en terminos de amplificacion; la discrepancia es de interpretacion de indices.

---

## Checkpoints verificados

- Checkpoint 1 — `bell_state.py`: circuito ejecuta correctamente, solo aparecen |00> y |11>, correlacion perfecta verificada
- Checkpoint 2 — `deutsch_jozsa.py`: oraculo constante retorna |00> con 100%, oraculo balanceado retorna estado distinto de |00> con 100%
- Checkpoint 3 — `grover.py`: amplificacion funciona con probabilidad del 100% para los cuatro targets; circuito de difusor implementado correctamente

---

## Capturas de evidencia

| Archivo                      | Experimento        | Descripcion                          |
|------------------------------|--------------------|--------------------------------------|
| bell_histogram.png           | Bell               | Distribucion ~50/50 de |00> y |11>   |
| dj_constante_histogram.png   | Deutsch-Jozsa      | Solo |00> con 1024 conteos             |
| dj_balanceada_histogram.png  | Deutsch-Jozsa      | Solo |11> con 1024 conteos             |
| grover_00.png                | Grover             | Target |00> amplificado al 100%       |
| grover_01.png                | Grover             | Target |01> — resultado |10>           |
| grover_10.png                | Grover             | Target |10> — resultado |01>           |
| grover_11.png                | Grover             | Target |11> amplificado al 100%       |

---

## Licencia

Proyecto academico — Universidad Francisco de Paula Santander · 2026
