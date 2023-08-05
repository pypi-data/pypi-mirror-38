# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import with_statement
from __future__ import absolute_import
from typing import Sequence

import numpy as np
import pytest

import cirq


def test_apply_unitary_to_tensor_presence_absence():
    m = np.array([[1, 0], [0, -1]])

    class NoUnitaryEffect(object):
        pass

    class HasUnitary(object):
        def _unitary_(self):
            return m

    class HasApplyReturnsNotImplemented(object):
        def _apply_unitary_to_tensor_(self,
                                      target_tensor,
                                      available_buffer,
                                      axes):
            return NotImplemented

    class HasApplyReturnsNotImplementedButHasUnitary(object):
        def _apply_unitary_to_tensor_(self,
                                      target_tensor,
                                      available_buffer,
                                      axes):
            return NotImplemented

        def _unitary_(self):
            print u"UNITARY"
            return m

    class HasApplyOutputInBuffer(object):
        def _apply_unitary_to_tensor_(self,
                                      target_tensor,
                                      available_buffer,
                                      axes,
                                      ):
            zero = cirq.slice_for_qubits_equal_to(axes, 0)
            one = cirq.slice_for_qubits_equal_to(axes, 1)
            available_buffer[zero] = target_tensor[zero]
            available_buffer[one] = -target_tensor[one]
            return available_buffer

    class HasApplyMutateInline(object):
        def _apply_unitary_to_tensor_(self,
                                      target_tensor,
                                      available_buffer,
                                      axes,
                                      ):
            one = cirq.slice_for_qubits_equal_to(axes, 1)
            target_tensor[one] *= -1
            return target_tensor

    fails = [
        NoUnitaryEffect(),
        HasApplyReturnsNotImplemented(),
    ]
    passes = [
        HasUnitary(),
        HasApplyReturnsNotImplementedButHasUnitary(),
        HasApplyOutputInBuffer(),
        HasApplyMutateInline(),
    ]

    def make_input():
        return np.array([1, 1, 1, 1], dtype=np.complex128).reshape((2, 2))

    def assert_works(val):
        expected_outputs = [
            np.array([1, 1, -1, -1]).reshape((2, 2)),
            np.array([1, -1, 1, -1]).reshape((2, 2)),
        ]
        for axis in xrange(2):
            result = cirq.apply_unitary_to_tensor(
                val, make_input(), buf, [axis])
            np.testing.assert_allclose(result, expected_outputs[axis])

    buf = np.empty(shape=(2, 2), dtype=np.complex128)

    for f in fails:
        with pytest.raises(TypeError, match=u'no _apply_unitary_to_tensor_'):
            _ = cirq.apply_unitary_to_tensor(f, make_input(), buf, [0])
        assert cirq.apply_unitary_to_tensor(
            f, make_input(), buf, [0], default=None) is None
        assert cirq.apply_unitary_to_tensor(
            f, make_input(), buf, [0], default=NotImplemented) is NotImplemented
        assert cirq.apply_unitary_to_tensor(
            f, make_input(), buf, [0], default=1) == 1

    for s in passes:
        assert_works(s)
        assert cirq.apply_unitary_to_tensor(
            s, make_input(), buf, [0], default=None) is not None
