# src/bell_state.py
# Experimento 1: Estado de Bell |Φ+⟩ — Entrelazamiento Cuántico
# Unidad 12: Computación Emergente y Tendencias
# Arquitectura de Computadores — UFPS 2026

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os


def bell_state_experiment(shots=1024):
    """
    Prepara el estado de Bell |Φ+⟩ = (|00⟩ + |11⟩)/√2 y mide.

    Circuito:
        q0: ─ H ─ ●─ M
        q1: ───── X─ M

    Resultado esperado: ~50% |00⟩ y ~50% |11⟩ (nunca |01⟩ ni |10⟩)
    """
    # Crear circuito: 2 qubits, 2 bits clásicos
    qc = QuantumCircuit(2, 2)

    # Paso 1: Hadamard en qubit 0 → superposición |+⟩
    qc.h(0)

    # Paso 2: CNOT (control=0, target=1) → entrelazamiento
    qc.cx(0, 1)

    # Paso 3: medir ambos qubits en la base computacional
    qc.measure([0, 1], [0, 1])

    # Simular con AerSimulator (no requiere hardware real)
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots)
    counts = job.result().get_counts()

    # Mostrar resultados
    print(f"\n{'='*45}")
    print(f"Resultados Estado de Bell |Φ+⟩ ({shots} shots):")
    print(f"{'='*45}")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        bar = "█" * int(pct / 2)
        print(f"  |{state}⟩ : {count:4d} ({pct:5.1f}%)  {bar}")

    # Verificación de correlación perfecta: solo |00⟩ y |11⟩
    assert "01" not in counts and "10" not in counts, \
        "ERROR: aparecieron estados no entrelazados (|01⟩ o |10⟩)"
    print("\n✓ OK: correlación perfecta verificada — entrelazamiento cuántico confirmado")
    print(f"\nDiagrama del circuito:\n{qc.draw()}")

    # Guardar histograma en carpeta capturas/
    os.makedirs("capturas", exist_ok=True)
    fig = plot_histogram(counts, title="Estado de Bell |Φ+⟩")
    fig.savefig("capturas/bell_histogram.png", dpi=150, bbox_inches="tight")
    print("\nHistograma guardado en: capturas/bell_histogram.png")
    plt.close(fig)

    return counts


if __name__ == "__main__":
    bell_state_experiment()
