import sys

sys.path.append("../src/")

import pennylane as qml
from pennylane import numpy as np

from bungalowbill import Bungalow


if __name__ == "__main__":

    dev = qml.device("default.qubit", wires=2)

    # error when diff_method = 'adjoint' is used: pennylane.QuantumFunctionError: Adjoint differentiation method does not support measurement state
    @qml.qnode(dev)
    def circuit(angles):
        qml.BasisState(np.array([1, 1]), wires=[0, 1])
        qml.broadcast(unitary=qml.PauliY, wires=range(2), pattern="single")
        qml.RY(angles[0], wires=0)
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.RX(angles[1], wires=1)
        return qml.expval(qml.PauliY(wires=0) @ qml.PauliX(wires=1))

    # some random test angles
    theta = np.pi / 10
    phi = np.pi * np.pi
    angles = np.array([theta, phi], requires_grad=True)

    path = "test.pt"
    bill = Bungalow(path)
    bill.save(
        circuit,
        path,
        dev,
        angles,
        metadata={"cats": "awesome", "dogs": "also awesome"},
    )

    dev, layer = bill.load_qnode(path)

    @qml.qnode(dev)
    def loaded_circuit():
        layer()
        return qml.expval(qml.PauliY(wires=0) @ qml.PauliX(wires=1))

    print("Truth check")
    print(circuit(angles) == loaded_circuit())

    print("\nGradient check")
    original_grad = qml.grad(circuit)(angles)
    loaded_grad = qml.grad(loaded_circuit)()
    print("Original gradient:", original_grad)
    print("Loaded gradient:", loaded_grad)
