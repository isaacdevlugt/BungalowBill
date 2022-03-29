import pennylane as qml
from collections import defaultdict, namedtuple

import pickle


class Bungalow:
    def __init__(self, path):
        self.path = path

    def operation_from_dict(self, op_dict):
        # given the result of gate.__dict__, re-create the 'gate' variable.
        return getattr(qml, op_dict["_name"])(*op_dict["data"], wires=op_dict["_wires"])

    def gates(self, circuit, *args, **kwargs):
        circuit(*args)
        tape = circuit.qtape

        gate_dict = defaultdict(dict)

        for i, op in enumerate(tape.operations):
            gate_dict[i] = op.__dict__

        return gate_dict

    def save(self, circuit, path, device, *args, metadata=None, **kwargs):
        # TODO: assert that circuit is a qnode
        # TODO: grab number of wires
        # TODO: grab device type
        gate_dict = self.gates(circuit, *args, **kwargs)
        gate_dict["device"] = device

        if metadata != None:
            gate_dict["metadata"] = metadata

        with open(path, "wb") as f:
            # TODO: try, except
            pickle.dump(gate_dict, f)

    def load_qnode(self, path, **kwargs):
        # should return the qnode function
        # **kwargs should contain stuff like gradient recipe, device, etc
        with open(path, "rb") as f:
            op_dict = pickle.load(f)

        def layer():
            # operations = []
            for key in op_dict.keys():
                if isinstance(key, int):
                    # operation = self.operation_from_dict(op_dict[key])
                    # operations.append(operation)
                    self.operation_from_dict(op_dict[key])

        return op_dict["device"], layer

