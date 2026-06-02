# src/deutsch_jozsa.py
# Experimento 2: Algoritmo de Deutsch-Jozsa
# Unidad 12: Computación Emergente y Tendencias
# Arquitectura de Computadores — UFPS 2026

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os


def oracle_constante(n):
    """
    Oráculo constante: f(x) = 0 para toda entrada.
    No aplica ninguna puerta → el ancilla no cambia.
    """
    return QuantumCircuit(n + 1)  # ancilla qubit incluido


def oracle_balanceada(n):
    """
    Oráculo balanceado para n=2:
    Aplica CNOT de cada qubit de entrada al ancilla.
    f(x) = 0 para exactamente la mitad de entradas,
           1 para la otra mitad.
    """
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.cx(i, n)  # CNOT: qubit_i → ancilla
    return qc


def deutsch_jozsa(oracle_qc, n, shots=1024, nombre_oraculo=""):
    """
    Ejecuta el algoritmo Deutsch-Jozsa con el oráculo dado.

    Circuito (n=2):
        q0: ─ H ─ [oráculo] ─ H ─ M
        q1: ─ H ─ [oráculo] ─ H ─ M
        q2: X ─ H ─ [oráculo] ─────  (ancilla, no se mide)

    Resultado:
        Todo |0...0⟩  → función CONSTANTE
        Algún |1⟩     → función BALANCEADA
    """
    qc = QuantumCircuit(n + 1, n)

    # Inicializar ancilla en |1⟩ → luego H lo lleva a |−⟩
    qc.x(n)

    # Aplicar Hadamard a todos los qubits (superposición uniforme)
    qc.h(range(n + 1))

    # Separador visual en el diagrama
    qc.barrier()

    # Aplicar oráculo (constante o balanceado)
    qc.compose(oracle_qc, inplace=True)

    qc.barrier()

    # Interferencia: Hadamard en los qubits de entrada
    qc.h(range(n))

    # Medir solo los qubits de entrada (no el ancilla)
    qc.measure(range(n), range(n))

    # Simular
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()

    # Mostrar resultados
    estado_todo_cero = "0" * n
    es_constante = estado_todo_cero in counts and len(counts) == 1

    print(f"\n{'='*45}")
    print(f"Deutsch-Jozsa — Oráculo: {nombre_oraculo} ({shots} shots)")
    print(f"{'='*45}")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        print(f"  |{state}⟩ : {count:4d} ({pct:5.1f}%)")

    if es_constante:
        print(f"\n→ Resultado: CONSTANTE (solo |{'0'*n}⟩ medido)")
    else:
        print(f"\n→ Resultado: BALANCEADA (aparecen estados ≠ |{'0'*n}⟩)")

    return counts


if __name__ == "__main__":
    n = 2  # número de qubits de entrada

    print("\n" + "="*50)
    print("ALGORITMO DE DEUTSCH-JOZSA (n=2 qubits)")
    print("="*50)
    print("Ventaja cuántica: 1 evaluación del oráculo")
    print(f"Clásico (peor caso): {2**(n-1) + 1} evaluaciones para n={n}")

    # --- Oráculo CONSTANTE ---
    counts_c = deutsch_jozsa(oracle_constante(n), n,
                              nombre_oraculo="CONSTANTE f(x)=0")

    # Verificación: debe retornar únicamente |00⟩
    assert "00" in counts_c and len(counts_c) == 1, \
        "ERROR: oráculo constante no retornó exclusivamente |00⟩"
    print("✓ OK: oráculo constante verificado correctamente")

    # --- Oráculo BALANCEADO ---
    counts_b = deutsch_jozsa(oracle_balanceada(n), n,
                              nombre_oraculo="BALANCEADA")

    # Verificación: NO debe aparecer |00⟩
    assert "00" not in counts_b, \
        "ERROR: oráculo balanceado retornó |00⟩ (debería ser balanceado)"
    print("✓ OK: oráculo balanceado verificado correctamente")

    # Guardar histogramas
    os.makedirs("capturas", exist_ok=True)

    fig_c = plot_histogram(counts_c, title="Deutsch-Jozsa — Oráculo Constante")
    fig_c.savefig("capturas/dj_constante_histogram.png", dpi=150, bbox_inches="tight")
    plt.close(fig_c)

    fig_b = plot_histogram(counts_b, title="Deutsch-Jozsa — Oráculo Balanceado")
    fig_b.savefig("capturas/dj_balanceada_histogram.png", dpi=150, bbox_inches="tight")
    plt.close(fig_b)

    print("\nHistogramas guardados en capturas/")
    print("\n✓ Deutsch-Jozsa: ambos oráculos verificados correctamente")
