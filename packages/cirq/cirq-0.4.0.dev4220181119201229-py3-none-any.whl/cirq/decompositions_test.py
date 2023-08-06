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

import cmath
import math
import random
from typing import Sequence

import numpy as np
import pytest

import cirq

def _operations_to_matrix(operations, qubits):
    return cirq.Circuit.from_ops(operations).to_unitary_matrix(
        qubit_order=cirq.QubitOrder.explicit(qubits),
        qubits_that_should_be_present=qubits)


def assert_gates_implement_unitary(gates: Sequence[cirq.SingleQubitGate],
                                   intended_effect: np.ndarray,
                                   atol: float):
    actual_effect = cirq.dot(*[cirq.unitary(g) for g in reversed(gates)])
    cirq.testing.assert_allclose_up_to_global_phase(actual_effect,
                                                    intended_effect,
                                                    atol=atol)


def test_single_qubit_matrix_to_gates_known_x():
    actual = cirq.single_qubit_matrix_to_gates(
        np.array([[0, 1], [1, 0]]), tolerance=0.01)

    assert actual == [cirq.X]


def test_single_qubit_matrix_to_gates_known_y():
    actual = cirq.single_qubit_matrix_to_gates(
        np.array([[0, -1j], [1j, 0]]), tolerance=0.01)

    assert actual == [cirq.Y]


def test_single_qubit_matrix_to_gates_known_z():
    actual = cirq.single_qubit_matrix_to_gates(
        np.array([[1, 0], [0, -1]]), tolerance=0.01)

    assert actual == [cirq.Z]


def test_single_qubit_matrix_to_gates_known_s():
    actual = cirq.single_qubit_matrix_to_gates(
        np.array([[1, 0], [0, 1j]]), tolerance=0.01)

    assert actual == [cirq.Z**0.5]


def test_known_s_dag():
    actual = cirq.single_qubit_matrix_to_gates(
        np.array([[1, 0], [0, -1j]]), tolerance=0.01)

    assert actual == [cirq.Z**-0.5]


def test_known_h():
    actual = cirq.single_qubit_matrix_to_gates(
        np.array([[1, 1], [1, -1]]) * np.sqrt(0.5), tolerance=0.001)

    assert actual == [cirq.Y**-0.5, cirq.Z]


@pytest.mark.parametrize('intended_effect', [
    np.array([[0, 1j], [1, 0]]),
    # Historical failure:
    np.array([[-0.10313355-0.62283483j,  0.76512225-0.1266025j],
              [-0.72184177+0.28352196j,  0.23073193+0.5876415j]]),
] + [
    cirq.testing.random_unitary(2) for _ in range(10)
])
def test_single_qubit_matrix_to_gates_cases(intended_effect):
    for atol in [1e-1, 1e-8]:
        gates = cirq.single_qubit_matrix_to_gates(
            intended_effect, tolerance=atol / 10)
        assert len(gates) <= 3
        assert sum(1 for g in gates if not isinstance(g, cirq.ZPowGate)) <= 1
        assert_gates_implement_unitary(gates, intended_effect, atol=atol)


@pytest.mark.parametrize('pre_turns,post_turns',
                         [(random.random(), random.random())
                          for _ in range(10)])
def test_single_qubit_matrix_to_gates_fuzz_half_turns_merge_z_gates(
        pre_turns, post_turns):
    intended_effect = cirq.dot(
        cirq.unitary(cirq.Z**(2 * pre_turns)),
        cirq.unitary(cirq.X),
        cirq.unitary(cirq.Z**(2 * post_turns)))

    gates = cirq.single_qubit_matrix_to_gates(
        intended_effect, tolerance=1e-7)

    assert len(gates) <= 2
    assert_gates_implement_unitary(gates, intended_effect, atol=1e-6)


def test_single_qubit_matrix_to_gates_tolerance_z():
    z = np.diag([1, np.exp(1j * 0.01)])

    optimized_away = cirq.single_qubit_matrix_to_gates(
        z, tolerance=0.1)
    assert len(optimized_away) == 0

    kept = cirq.single_qubit_matrix_to_gates(z, tolerance=0.0001)
    assert len(kept) == 1


def test_single_qubit_matrix_to_gates_tolerance_xy():
    c, s = np.cos(0.01), np.sin(0.01)
    xy = np.array([[c, -s], [s, c]])

    optimized_away = cirq.single_qubit_matrix_to_gates(
        xy, tolerance=0.1)
    assert len(optimized_away) == 0

    kept = cirq.single_qubit_matrix_to_gates(xy, tolerance=0.0001)
    assert len(kept) == 1


def test_single_qubit_matrix_to_gates_tolerance_half_turn_phasing():
    a = np.pi / 2 + 0.01
    c, s = np.cos(a), np.sin(a)
    nearly_x = np.array([[c, -s], [s, c]])
    z1 = np.diag([1, np.exp(1j * 1.2)])
    z2 = np.diag([1, np.exp(1j * 1.6)])
    phased_nearly_x = z1.dot(nearly_x).dot(z2)

    optimized_away = cirq.single_qubit_matrix_to_gates(
        phased_nearly_x, tolerance=0.1)
    assert len(optimized_away) == 2

    kept = cirq.single_qubit_matrix_to_gates(
        phased_nearly_x, tolerance=0.0001)
    assert len(kept) == 3


def test_single_qubit_op_to_framed_phase_form_output_on_example_case():
    u, t, g = cirq.single_qubit_op_to_framed_phase_form(
        cirq.unitary(cirq.Y**0.25))
    assert cirq.allclose_up_to_global_phase(u, cirq.unitary(cirq.X**0.5))
    assert abs(t - (1 + 1j) * math.sqrt(0.5)) < 0.00001
    assert abs(g - 1) < 0.00001


@pytest.mark.parametrize('mat', [
    np.eye(2),
    cirq.unitary(cirq.H),
    cirq.unitary(cirq.X),
    cirq.unitary(cirq.X**0.5),
    cirq.unitary(cirq.Y),
    cirq.unitary(cirq.Z),
    cirq.unitary(cirq.Z**0.5),
] + [cirq.testing.random_unitary(2)
     for _ in range(10)])
def test_single_qubit_op_to_framed_phase_form_equivalent_on_known_and_random(
        mat):
    u, t, g = cirq.single_qubit_op_to_framed_phase_form(mat)
    z = np.diag([g, g * t])
    assert np.allclose(mat, np.conj(u.T).dot(z).dot(u))


def test_controlled_op_to_operations_concrete_case():
    c = cirq.NamedQubit('c')
    t = cirq.NamedQubit('t')
    expected = [cirq.Y(t)**-0.5, cirq.CZ(c, t)**1.5,
                cirq.Z(c)**0.25, cirq.Y(t)**0.5]
    operations = cirq.controlled_op_to_operations(
        control=c,
        target=t,
        operation=np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5),
        tolerance=0.0001)
    # Test closeness as opposed to equality to avoid precision errors
    for actual_op, expected_op in zip(operations, expected):
        assert cirq.allclose_up_to_global_phase(cirq.unitary(actual_op),
                                                cirq.unitary(expected_op),
                                                atol=1e-8)

def test_controlled_op_to_operations_omits_negligible_global_phase():
    qc = cirq.NamedQubit('c')
    qt = cirq.NamedQubit('qt')
    operations = cirq.controlled_op_to_operations(
        control=qc,
        target=qt,
        operation=cirq.unitary(cirq.H),
        tolerance=0.0001)

    assert operations == [cirq.Y(qt)**-0.25, cirq.CZ(qc, qt), cirq.Y(qt)**0.25]


@pytest.mark.parametrize('mat', [
    np.eye(2),
    cirq.unitary(cirq.H),
    cirq.unitary(cirq.X),
    cirq.unitary(cirq.X**0.5),
    cirq.unitary(cirq.Y),
    cirq.unitary(cirq.Z),
    cirq.unitary(cirq.Z**0.5),
] + [
    cirq.testing.random_unitary(2) for _ in range(10)
])
def test_controlled_op_to_operations_equivalent_on_known_and_random(mat):
    qc = cirq.NamedQubit('c')
    qt = cirq.NamedQubit('qt')
    operations = cirq.controlled_op_to_operations(
        control=qc, target=qt, operation=mat)
    actual_effect = _operations_to_matrix(operations, (qc, qt))
    intended_effect = cirq.kron_with_controls(cirq.CONTROL_TAG, mat)
    assert cirq.allclose_up_to_global_phase(actual_effect, intended_effect)


def _random_single_partial_cz_effect():
    return cirq.dot(
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)),
        np.diag([1, 1, 1, cmath.exp(2j * random.random() * np.pi)]),
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)))


def _random_double_partial_cz_effect():
    return cirq.dot(
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)),
        np.diag([1, 1, 1, cmath.exp(2j * random.random() * np.pi)]),
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)),
        np.diag([1, 1, 1, cmath.exp(2j * random.random() * np.pi)]),
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)))


def _random_double_full_cz_effect():
    return cirq.dot(
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)),
        cirq.unitary(cirq.CZ),
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)),
        cirq.unitary(cirq.CZ),
        cirq.kron(cirq.testing.random_unitary(2),
                  cirq.testing.random_unitary(2)))


def assert_cz_depth_below(operations, threshold, must_be_full):
    total_cz = 0

    for op in operations:
        assert len(op.qubits) <= 2
        if len(op.qubits) == 2:
            assert isinstance(op, cirq.GateOperation)
            assert isinstance(op.gate, cirq.CZPowGate)
            if must_be_full:
                assert op.gate.exponent == 1
            total_cz += abs(op.gate.exponent)

    assert total_cz <= threshold


def assert_ops_implement_unitary(q0, q1, operations, intended_effect,
                                 atol=0.01):
    actual_effect = _operations_to_matrix(operations, (q0, q1))
    assert cirq.allclose_up_to_global_phase(actual_effect, intended_effect,
                                              atol=atol)


@pytest.mark.parametrize('max_partial_cz_depth,max_full_cz_depth,effect', [
    (0, 0, np.eye(4)),
    (0, 0, np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0j],
    ])),
    (0, 0, cirq.unitary(cirq.CZ**0.00000001)),

    (0.5, 2, cirq.unitary(cirq.CZ**0.5)),

    (1, 1, cirq.unitary(cirq.CZ)),
    (1, 1, cirq.unitary(cirq.CNOT)),
    (1, 1, np.array([
        [1, 0, 0, 1j],
        [0, 1, 1j, 0],
        [0, 1j, 1, 0],
        [1j, 0, 0, 1],
    ]) * np.sqrt(0.5)),
    (1, 1, np.array([
        [1, 0, 0, -1j],
        [0, 1, -1j, 0],
        [0, -1j, 1, 0],
        [-1j, 0, 0, 1],
    ]) * np.sqrt(0.5)),
    (1, 1, np.array([
        [1, 0, 0, 1j],
        [0, 1, -1j, 0],
        [0, -1j, 1, 0],
        [1j, 0, 0, 1],
    ]) * np.sqrt(0.5)),

    (1.5, 3, cirq.map_eigenvalues(cirq.unitary(cirq.SWAP),
                                  lambda e: e**0.5)),

    (2, 2, cirq.unitary(cirq.SWAP).dot(cirq.unitary(cirq.CZ))),

    (3, 3, cirq.unitary(cirq.SWAP)),
    (3, 3, np.array([
        [0, 0, 0, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0j],
    ])),
] + [
    (1, 2, _random_single_partial_cz_effect()) for _ in range(10)
] + [
    (2, 2, _random_double_full_cz_effect()) for _ in range(10)
] + [
    (2, 3, _random_double_partial_cz_effect()) for _ in range(10)
] + [
    (3, 3, cirq.testing.random_unitary(4)) for _ in range(10)
])
def test_two_to_ops_equivalent_and_bounded_for_known_and_random(
        max_partial_cz_depth,
        max_full_cz_depth,
        effect):
    q0 = cirq.NamedQubit('q0')
    q1 = cirq.NamedQubit('q1')

    operations_with_partial = cirq.two_qubit_matrix_to_operations(
        q0, q1, effect, True)
    operations_with_full = cirq.two_qubit_matrix_to_operations(
        q0, q1, effect, False)

    assert_ops_implement_unitary(q0, q1, operations_with_partial, effect)
    assert_ops_implement_unitary(q0, q1, operations_with_full, effect)

    assert_cz_depth_below(operations_with_partial, max_partial_cz_depth, False)
    assert_cz_depth_below(operations_with_full, max_full_cz_depth, True)


def test_trivial_parity_interaction_corner_case():
    q0 = cirq.NamedQubit('q0')
    q1 = cirq.NamedQubit('q1')
    nearPi4 = np.pi/4 * 0.99
    tolerance = 1e-2
    circuit = cirq.Circuit.from_ops(
        cirq.decompositions._parity_interaction(q0, q1, -nearPi4, tolerance))
    assert len(circuit) == 2


@pytest.mark.parametrize('rad,expected', (lambda err, largeErr: [
    (np.pi/4, True),
    (np.pi/4 + err, True),
    (np.pi/4 + largeErr, False),
    (np.pi/4 - err, True),
    (np.pi/4 - largeErr, False),
    (-np.pi/4, True),
    (-np.pi/4 + err, True),
    (-np.pi/4 + largeErr, False),
    (-np.pi/4 - err, True),
    (-np.pi/4 - largeErr, False),
    (0, True),
    (err, True),
    (largeErr, False),
    (-err, True),
    (-largeErr, False),
    (np.pi/8, False),
    (-np.pi/8, False),
])(1e-8*2/3, 1e-8*4/3))
def test_is_trivial_angle(rad, expected):
    tolerance = 1e-8
    out = cirq.decompositions._is_trivial_angle(rad, tolerance)
    assert out == expected, 'rad = {}'.format(rad)
