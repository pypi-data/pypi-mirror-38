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

from kmqc.base import Instruction


class Program(object):

    def __init__(self, *instructions):
        self.instructions = list()
        self.append_instruction(instructions)

    def append_instruction(self, *instructions):
        for instruction in instructions:
            if isinstance(instruction, list):
                self.append_instruction(*instruction)
            elif isinstance(instruction, tuple):
                self.append_instruction(*instruction)
            elif isinstance(instruction, Program):
                if id(self) != id(instruction):
                    for i in instruction:
                        self.append_instruction(i)
            elif isinstance(instruction, Instruction):
                self.instructions.append(instruction)
        return self

    def __add__(self, other):
        p = Program()
        p.append_instruction(self)
        p.append_instruction(other)
        return p

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __iter__(self):
        return self.instructions.__iter__()
