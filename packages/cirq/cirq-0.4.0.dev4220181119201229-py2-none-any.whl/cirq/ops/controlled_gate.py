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

from __future__ import absolute_import
from typing import Union, Sequence, Any

import numpy as np

from cirq import linalg, protocols, value
from cirq.ops import raw_types
from cirq.type_workarounds import NotImplementedType


class ControlledGate(raw_types.Gate):
    u"""Augments existing gates with a control qubit."""

    def __init__(self, sub_gate):
        u"""Initializes the controlled gate.

        Args:
            sub_gate: The gate to add a control qubit to.
        """
        self.sub_gate = sub_gate

    def validate_args(self, qubits):
        if len(qubits) < 1:
            raise ValueError(u'No control qubit specified.')
        self.sub_gate.validate_args(qubits[1:])

    def _value_equality_values_(self):
        return self.sub_gate

    def _apply_unitary_to_tensor_(self,
                                  target_tensor,
                                  available_buffer,
                                  axes,
                                  ):
        control = axes[0]
        rest = axes[1:]
        active = linalg.slice_for_qubits_equal_to([control], 1)
        sub_axes = [r - int(r > control) for r in rest]
        target_view = target_tensor[active]
        buffer_view = available_buffer[active]
        result = protocols.apply_unitary_to_tensor(
            self.sub_gate,
            target_view,
            buffer_view,
            sub_axes,
            default=NotImplemented)

        if result is NotImplemented:
            return NotImplemented

        if result is target_view:
            return target_tensor

        if result is buffer_view:
            inactive = linalg.slice_for_qubits_equal_to([control], 0)
            available_buffer[inactive] = target_tensor[inactive]
            return available_buffer

        # HACK: assume they didn't somehow escape the slice view and edit the
        # rest of target_tensor.
        target_tensor[active] = result
        return target_tensor

    def _has_unitary_(self):
        return protocols.has_unitary(self.sub_gate)

    def _unitary_(self):
        sub_matrix = protocols.unitary(self.sub_gate, None)
        if sub_matrix is None:
            return NotImplemented
        return linalg.block_diag(np.eye(sub_matrix.shape[0]), sub_matrix)

    def __pow__(self, exponent):
        new_sub_gate = protocols.pow(self.sub_gate,
                                     exponent,
                                     NotImplemented)
        if new_sub_gate is NotImplemented:
            return NotImplemented
        return ControlledGate(new_sub_gate)

    def _is_parameterized_(self):
        return protocols.is_parameterized(self.sub_gate)

    def _resolve_parameters_(self, param_resolver):
        new_sub_gate = protocols.resolve_parameters(self.sub_gate,
                                                    param_resolver)
        return ControlledGate(new_sub_gate)

    def _trace_distance_bound_(self):
        return protocols.trace_distance_bound(self.sub_gate)

    def _circuit_diagram_info_(self,
                               args
                               ):
        sub_info = protocols.circuit_diagram_info(self.sub_gate, args, None)
        if sub_info is None:
            return NotImplemented
        return protocols.CircuitDiagramInfo(
            wire_symbols=(u'@',) + sub_info.wire_symbols,
            exponent=sub_info.exponent)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'C' + unicode(self.sub_gate)

    def __repr__(self):
        return u'cirq.ControlledGate(sub_gate={!r})'.format(self.sub_gate)

ControlledGate = value.value_equality(ControlledGate)
