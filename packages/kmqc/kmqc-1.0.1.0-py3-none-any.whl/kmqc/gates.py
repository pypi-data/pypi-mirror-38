# Copyright (C) 2018 Rustam Sayfutdinov, rstm.sf@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math

from six import integer_types

from kmqc.base import Gate, Qubit


def _to_qubit(qubit):
    if isinstance(qubit, integer_types):
        return Qubit(qubit)
    elif isinstance(qubit, Qubit):
        return qubit
    else:
        raise TypeError('Кубит должен быть целого типа или Qubit!')


class Rx(Gate):
    """
    Rx(mu) = [[cos(mu / 2), -1j * sin(mu / 2)],
               [-1j * sin(mu / 2), cos(mu / 2)]]
    """

    def __init__(self, mu, qubit):
        params = {'mu': mu, }
        super().__init__('Rx', params, [_to_qubit(qubit), ])


class Ry(Gate):
    """
    Ry(theta) = [[cos(theta / 2), -sin(theta / 2)],
                 [sin(theta / 2), cos(theta / 2)]]
    """

    def __init__(self, theta, qubit):
        params = {'theta': theta, }
        super().__init__('Ry', params, [_to_qubit(qubit), ])


class Rz(Gate):
    """
    Rz(phi) = [[exp(-1j * phi / 2), 0]
               [0, exp(1j * phi / 2)]]
    """

    def __init__(self, phi, qubit):
        params = {'phi': phi, }
        super().__init__('Rz', params, [_to_qubit(qubit), ])


class U1(Gate):
    """
    U1(mu) = [[1, 0],
               [0, exp(1j * mu)]]
    """

    def __init__(self, mu, qubit):
        params = {'mu': mu, }
        super().__init__('U1', params, [_to_qubit(qubit), ])


class U2(Gate):
    """
    U2(mu) = Rz(phi + pi / 2) Rx(pi / 2) Rz(mu - pi / 2)
    """

    def __init__(self, phi, mu, qubit):
        params = {'phi': phi, 'mu': mu, }
        super().__init__('U2', params, [_to_qubit(qubit), ])


class U3(Gate):
    """
    U3(mu) = Rz(phi + 3 * pi) Rx(pi / 2) Rz(theta + pi) Rx(pi / 2) Rz(mu)
    """

    def __init__(self, theta, phi, mu, qubit):
        params = {'theta': theta, 'phi': phi, 'mu': mu, }
        super().__init__('U3', params, [_to_qubit(qubit), ])


class Z(U1):
    """
    Z = [[1, 0],
         [0, -1]]
    """

    def __init__(self, qibit):
        super().__init__(math.pi, qibit)


class S_H(U1):
    """
    S = [[1, 0],
         [0, -1j]]
    """

    def __init__(self, qibit):
        super().__init__(-math.pi / 2.0, qibit)


class X(U3):
    """
    X = [[0, 1],
         [1, 0]]
    """

    def __init__(self, qibit):
        super().__init__(math.pi, 0.0, math.pi, qibit)


class Y(U3):
    """
    Y = [[0, 0 - 1j],
         [0 + 1j, 0]]
    """

    def __init__(self, qibit):
        super().__init__(math.pi, math.pi / 2.0, math.pi / 2.0, qibit)


def _make_gate(name, count_qubits):
    def gate():
        def constructor(*qubits):
            qubits = list(qubits)
            if len(qubits) != count_qubits:
                raise ValueError(
                    'Количество кубитов для {} должно равняться {}!'.format(
                        name, count_qubits))
            return Gate(name, None, [_to_qubit(q) for q in qubits])
        return constructor
    return gate


H = _make_gate('Hadamard', 1)()
"""
H = sqrt(2) / 2 * [[1, 1],
                   [1, -1]]
"""

S = _make_gate('S', 1)()
"""
S = [[1, 0],
     [0, 1j]]
"""

T = _make_gate('T', 1)()
"""
T = [[1, 0],
     [0, exp(1j * pi / 4)]]
"""

T_H = _make_gate('THerm', 1)()
"""
T = T ^ H = [[1, 0],
             [0, exp(-1j * pi / 4)]]
"""

CNOT = _make_gate('CNOT', 2)()
"""
CNOT = [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]]
"""

CCNOT = _make_gate('CCNOT', 3)()
"""
CCNOT = [[1, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 1, 0]]
"""

DEFINITE_GATES = {
    'Rx': Rx,
    'Ry': Ry,
    'Rz': Rz,
    'U1': U1,
    'U2': U2,
    'U3': U3,
    'H': H,
    'S': S,
    'S_H': S_H,
    'T': T,
    'T_H': T_H,
    'X': X,
    'Y': Y,
    'Z': Z,
    'CNOT': CNOT,
    'CCNOT': CCNOT,
}
