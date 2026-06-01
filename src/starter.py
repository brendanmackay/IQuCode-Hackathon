"""Small Qiskit sanity check for the hackathon workspace."""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def build_bell_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def main() -> None:
    circuit = build_bell_circuit()
    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)
    result = simulator.run(compiled, shots=1024).result()
    counts = result.get_counts()

    print(circuit)
    print("Counts:", counts)


if __name__ == "__main__":
    main()
