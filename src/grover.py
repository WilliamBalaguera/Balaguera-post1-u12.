# src/grover.py
# Experimento 3: Algoritmo de Grover en 2 Qubits
# Unidad 12: Computación Emergente y Tendencias
# Arquitectura de Computadores — UFPS 2026

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os


def grover_2qubits(target="11", shots=1024):
    """
    Implementa el algoritmo de Grover para n=2 qubits.

    Parámetros:
        target (str): estado objetivo en binario ('00', '01', '10', '11')
        shots  (int): número de mediciones

    Circuito:
        1. Superposición uniforme: H ⊗ H
        2. Oráculo de fase: marca el estado target con fase -1
        3. Difusor (inversión alrededor de la media): amplifica target

    Para n=2 qubits, 1 iteración es óptima → probabilidad ~100% del target.
    """
    if target not in ["00", "01", "10", "11"]:
        raise ValueError(f"Target '{target}' no válido. Use '00', '01', '10' o '11'.")

    qc = QuantumCircuit(2, 2)

    # ── PASO 1: Superposición uniforme ────────────────────────────────────────
    qc.h([0, 1])
    qc.barrier(label="superposición")

    # ── PASO 2: Oráculo de fase ───────────────────────────────────────────────
    # Invierte la fase del estado target: |target⟩ → -|target⟩
    # Implementación: X en qubits que son 0 en el target → CZ → X de vuelta
    if target == "11":
        # CZ aplica fase -1 directamente a |11⟩
        qc.cz(0, 1)
    elif target == "00":
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])
    elif target == "01":
        # qubit 0 es 0 → X en q0, CZ, X en q0
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)
    elif target == "10":
        # qubit 1 es 0 → X en q1, CZ, X en q1
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)

    qc.barrier(label="oráculo")

    # ── PASO 3: Difusor (inversión alrededor de la media) ────────────────────
    # D = H X CZ X H  (equivalente a 2|s⟩⟨s| - I)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    qc.barrier(label="difusor")

    # ── MEDICIÓN ──────────────────────────────────────────────────────────────
    qc.measure([0, 1], [0, 1])

    # Simular
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()

    # Mostrar resultados
    print(f"\n{'='*48}")
    print(f"Grover 2 qubits — buscando |{target}⟩  ({shots} shots)")
    print(f"{'='*48}")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        bar = "█" * int(pct / 2)
        marca = " ← TARGET" if state == target else ""
        print(f"  |{state}⟩ : {count:4d} ({pct:5.1f}%)  {bar}{marca}")

    top = max(counts, key=counts.get)
    prob_top = counts[top] / shots * 100
    correcto = top == target
    simbolo = "✓" if correcto else "✗"
    print(f"\n{simbolo} Estado más probable: |{top}⟩ ({prob_top:.1f}%) — "
          f"{'CORRECTO' if correcto else 'ERROR'}")

    # Guardar histograma
    os.makedirs("capturas", exist_ok=True)
    fig = plot_histogram(counts, title=f"Grover — Buscando |{target}⟩")
    fig.savefig(f"capturas/grover_{target}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    return counts, correcto


if __name__ == "__main__":
    print("\n" + "="*50)
    print("ALGORITMO DE GROVER — 2 QUBITS (4 estados)")
    print("="*50)
    print("Espacio de búsqueda: {|00⟩, |01⟩, |10⟩, |11⟩}")
    print("Iteraciones óptimas para n=2: 1")
    print("Aceleración cuadrática: O(√N) vs O(N) clásico")

    resultados = {}
    todos_correctos = True

    for t in ["00", "01", "10", "11"]:
        counts, correcto = grover_2qubits(target=t)
        resultados[t] = counts
        if not correcto:
            todos_correctos = False

    # Resumen final
    print("\n" + "="*50)
    print("RESUMEN — Probabilidad del estado target")
    print("="*50)
    print(f"{'Target':<8} {'P(target)':<12} {'Veredicto'}")
    print("-"*35)
    for t, counts in resultados.items():
        prob = counts.get(t, 0) / 1024 * 100
        ok = "✓ CORRECTO" if counts.get(t, 0) == max(counts.values()) else "✗ ERROR"
        print(f"  |{t}⟩    {prob:6.1f}%      {ok}")

    print("\n" + ("✓ Todos los targets encontrados correctamente."
                  if todos_correctos else "✗ Algunos targets fallaron."))
    print("Histogramas guardados en capturas/grover_XX.png")
