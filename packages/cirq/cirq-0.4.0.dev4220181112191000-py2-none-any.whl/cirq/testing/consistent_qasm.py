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
import warnings
from typing import Any

from cirq import protocols, ops, line, circuits, linalg
from cirq.testing import lin_alg_utils


def assert_qasm_is_consistent_with_unitary(val):
    u"""Uses `val._unitary_` to check `val._qasm_`'s behavior."""

    # Only test if qiskit is installed.
    try:
        import qiskit
    except ImportError:
        # coverage: ignore
        warnings.warn(u"Skipped assert_qasm_is_consistent_with_unitary because "
                      u"qiskit isn't installed to verify against.")
        return

    unitary = protocols.unitary(val, None)
    if unitary is None:
        # Vacuous consistency.
        return

    qubit_count = len(unitary).bit_length() - 1
    if isinstance(val, ops.Operation):
        qubits = val.qubits
        op = val
    elif isinstance(val, ops.Gate):
        qubits = tuple(line.LineQubit.range(qubit_count))
        op = val.on(*qubits)
    else:
        raise NotImplementedError(u"Don't know how to test {!r}".format(val))

    qasm = unicode(circuits.QasmOutput(op, qubits[::-1], precision=10))

    qasm_unitary = None
    try:
        result = qiskit.execute(
            qiskit.load_qasm_string(qasm),
            backend=qiskit.Aer.get_backend(u'unitary_simulator'))
        qasm_unitary = result.result().get_unitary()

        lin_alg_utils.assert_allclose_up_to_global_phase(
            qasm_unitary,
            unitary,
            rtol=1e-8,
            atol=1e-8)
    except Exception, ex:
        if qasm_unitary is not None:
            p_unitary, p_qasm_unitary = linalg.match_global_phase(
                unitary, qasm_unitary)
        else:
            p_unitary = None
            p_qasm_unitary = None
        raise AssertionError(
            u'QASM be consistent with cirq.unitary(op) up to global phase.\n\n'
            u'op:\n{}\n\n'
            u'cirq.unitary(op):\n{}\n\n'
            u'Generated QASM:\n\n{}\n\n'
            u'Unitary of generated QASM:\n{}\n\n'
            u'Phased matched cirq.unitary(op):\n{}\n\n'
            u'Phased matched unitary of generated QASM:\n{}\n\n'
            u'Underlying error:\n{}'.format(
                _indent(repr(op)),
                _indent(repr(unitary)),
                _indent(qasm),
                _indent(repr(qasm_unitary)),
                _indent(repr(p_unitary)),
                _indent(repr(p_qasm_unitary)),
                _indent(unicode(ex))))


def _indent(*content):
    return u'    ' + u'\n'.join(content).replace(u'\n', u'\n    ')
