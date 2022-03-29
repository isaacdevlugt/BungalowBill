import pennylane as qml

n_bits = 3
dev = qml.device("lightning.qubit", wires=range(n_bits))


@qml.qnode(dev)
def circuit(theta):

    qml.CNOT(wires=[0, 1])
    qml.RZ(theta, wires=1)
    qml.Hadamard(wires=2)

    return qml.state()


def gates_of_circuit(circuit, args):

    circuit(args)

    """
    Args:
    - circuit (qNode)
    """

    tape = circuit.qtape

    for op in tape.operations:
        print(f"gate {op.name}\n.  wires {op.wires}\n.  params {op.parameters}\n")


args = 1.234
gates_of_circuit(circuit, args)
