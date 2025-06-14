import cmath

class Qubit:
    def __init__(self, state='0'):
        if state == '1':
            self.state = [complex(0), complex(1)]
        else:
            self.state = [complex(1), complex(0)]

    def apply(self, gate):
        new_state = [
            gate[0][0] * self.state[0] + gate[0][1] * self.state[1],
            gate[1][0] * self.state[0] + gate[1][1] * self.state[1]
        ]
        self.state = new_state

    def __str__(self):
        return f"[{self.state[0]:.4f}, {self.state[1]:.4f}]"


X = [[0, 1], [1, 0]]

Y = [[0, -1j], [1j, 0]]

Z = [[1, 0], [0, -1]]


def cnot(control_qubit, target_qubit):

    state = [
        control_qubit.state[0] * target_qubit.state[0],
        control_qubit.state[0] * target_qubit.state[1],
        control_qubit.state[1] * target_qubit.state[0],
        control_qubit.state[1] * target_qubit.state[1]
    ]

    CNOT_matrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ]

    new_state = [complex(0) for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_state[i] += CNOT_matrix[i][j] * state[j]

    control_qubit.state = [new_state[0], new_state[1]]
    target_qubit.state = [new_state[2], new_state[3]]

    return new_state

if __name__ == "__main__":
    print("Кубит |0>:", Qubit('0'))
    print("Кубит |1>:", Qubit('1'))

    print("\n--- Применение гейтов ---")
    q = Qubit('0')
    print("До X:", q)
    q.apply(X)
    print("После X:", q)

    q = Qubit('0')
    print("До Y:", q)
    q.apply(Y)
    print("После Y:", q)

    q = Qubit('0')
    print("До Z:", q)
    q.apply(Z)
    print("После Z:", q)

    print("\n--- Применение CNOT ---")
    control = Qubit('1')
    target = Qubit('0')

    print("До CNOT:")
    print("control:", control)
    print("target:", target)

    cnot(control, target)

    print("После CNOT:")
    print("control:", control)
    print("target:", target)