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

from six import integer_types, string_types


class Qubit(object):

    def __init__(self, index):
        if not isinstance(index, integer_types) and index < 0:
            raise TypeError('Инедкс должен быть целым неотрицательным числом!')
        self.index = index

    def __eq__(self, other):
        return isinstance(other, Qubit) and other.index == self.index

    def __ne__(self, other):
        return not self.__eq__(other)


class Instruction(object):
    """Абстрактный класс."""


class Gate(Instruction):

    def __init__(self, name, params, qubits):
        if not isinstance(name, string_types):
            raise TypeError('Название гейта должно быть строкового типа!')
        if not isinstance(qubits, list) or not qubits:
            raise TypeError('Кубиты должны передаваться в непустом списке!')
        for q in qubits:
            if not isinstance(q, Qubit):
                raise TypeError('Кубиты должны иметь тип Qubit!')
        self.name = name
        self.params = params
        self.qubits = qubits

    def to_circuit_json(self):
        params = None
        if isinstance(self.params, dict):
            params = {}
            for p in self.params.keys():
                params[p] = self.params[p]
        return {
            'operator': self.name,
            'qubits': [q.index for q in self.qubits],
            'params': params,
        }

    def count_qubits(self):
        return len(self.qubits)
