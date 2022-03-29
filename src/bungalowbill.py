import pennylane as qml
from collections import defaultdict, namedtuple

import pickle


class Bungalow:
    def __init__(self, path):
        self.path = path

    def op_from_dict(self, op_dict):
        return getattr(qml, op_dict["_name"])(*op_dict["data"], wires=op_dict["_wires"])

    def req_grad_op_from_dict(self, op_dict, arg):
        return getattr(qml, op_dict["_name"])(arg, wires=op_dict["_wires"])

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

        # grab all requires_grad data
        req_grad_args = []
        for key in op_dict.keys():
            if isinstance(key, int):
                if op_dict[key]["data"] and op_dict[key]["data"][0].requires_grad:
                    req_grad_args.append(op_dict[key]["data"][0])

        def layer(*args, j=0):
            for key in op_dict.keys():
                if isinstance(key, int):
                    if (
                        not op_dict[key]["data"]
                        or not op_dict[key]["data"][0].requires_grad
                    ):
                        self.op_from_dict(op_dict[key])
                    else:
                        self.req_grad_op_from_dict(op_dict[key], args[j])
                        j += 1

        return req_grad_args, op_dict["device"], layer
