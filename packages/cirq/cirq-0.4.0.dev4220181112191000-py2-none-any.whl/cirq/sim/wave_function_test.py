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
u"""Tests for wave_function.py"""

from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import itertools
import pytest

import numpy as np

import cirq


def assert_dirac_notation(vec, expected, decimals=2):
    assert cirq.dirac_notation(np.array(vec), decimals=decimals) == expected


def test_dirac_notation():
    sqrt = np.sqrt(0.5)
    exp_pi_2 = 0.5 + 0.5j
    assert_dirac_notation([1], u"|⟩")
    assert_dirac_notation([sqrt, sqrt], u"(0.71)|0⟩ + (0.71)|1⟩")
    assert_dirac_notation([-sqrt, sqrt], u"(-0.71)|0⟩ + (0.71)|1⟩")
    assert_dirac_notation([sqrt, -sqrt], u"(0.71)|0⟩ + (-0.71)|1⟩")
    assert_dirac_notation([-sqrt, -sqrt], u"(-0.71)|0⟩ + (-0.71)|1⟩")
    assert_dirac_notation([sqrt, 1j * sqrt], u"(0.71)|0⟩ + (0.71j)|1⟩")
    assert_dirac_notation([sqrt, exp_pi_2], u"(0.71)|0⟩ + (0.5+0.5j)|1⟩")
    assert_dirac_notation([exp_pi_2, -sqrt], u"(0.5+0.5j)|0⟩ + (-0.71)|1⟩")
    assert_dirac_notation([exp_pi_2, 0.5 - 0.5j],
                          u"(0.5+0.5j)|0⟩ + (0.5-0.5j)|1⟩")
    assert_dirac_notation([0.5, 0.5, -0.5, -0.5],
                        u"(0.5)|00⟩ + (0.5)|01⟩ + (-0.5)|10⟩ + (-0.5)|11⟩")


def test_dirac_notation_partial_state():
    sqrt = np.sqrt(0.5)
    exp_pi_2 = 0.5 + 0.5j
    assert_dirac_notation([1, 0], u"|0⟩")
    assert_dirac_notation([1j, 0], u"(1j)|0⟩")
    assert_dirac_notation([0, 1], u"|1⟩")
    assert_dirac_notation([0, 1j], u"(1j)|1⟩")
    assert_dirac_notation([sqrt, 0 , 0, sqrt], u"(0.71)|00⟩ + (0.71)|11⟩")
    assert_dirac_notation([sqrt, sqrt , 0, 0], u"(0.71)|00⟩ + (0.71)|01⟩")
    assert_dirac_notation([exp_pi_2, 0, 0, exp_pi_2],
                        u"(0.5+0.5j)|00⟩ + (0.5+0.5j)|11⟩")
    assert_dirac_notation([0, 0, 0, 1], u"|11⟩")


def test_dirac_notation_precision():
    sqrt = np.sqrt(0.5)
    assert_dirac_notation([sqrt, sqrt], u"(0.7)|0⟩ + (0.7)|1⟩", decimals=1)
    assert_dirac_notation([sqrt, sqrt], u"(0.707)|0⟩ + (0.707)|1⟩", decimals=3)



def test_to_valid_state_vector():
    np.testing.assert_almost_equal(cirq.to_valid_state_vector(
        np.array([1.0, 0.0, 0.0, 0.0], dtype=np.complex64), 2),
        np.array([1.0, 0.0, 0.0, 0.0]))
    np.testing.assert_almost_equal(cirq.to_valid_state_vector(
        np.array([0.0, 1.0, 0.0, 0.0], dtype=np.complex64), 2),
        np.array([0.0, 1.0, 0.0, 0.0]))
    np.testing.assert_almost_equal(cirq.to_valid_state_vector(0, 2),
                                   np.array([1.0, 0.0, 0.0, 0.0]))
    np.testing.assert_almost_equal(cirq.to_valid_state_vector(1, 2),
                                   np.array([0.0, 1.0, 0.0, 0.0]))


def test_invalid_to_valid_state_vector():
    with pytest.raises(ValueError):
        _ = cirq.to_valid_state_vector(
            np.array([1.0, 0.0], dtype=np.complex64), 2)
    with pytest.raises(ValueError):
        _ = cirq.to_valid_state_vector(-1, 2)
    with pytest.raises(ValueError):
        _ = cirq.to_valid_state_vector(5, 2)
    with pytest.raises(TypeError):
        _ = cirq.to_valid_state_vector(u'not an int', 2)


def test_check_state():
    cirq.validate_normalized_state(
        np.array([0.5, 0.5, 0.5, 0.5], dtype=np.complex64),
                                   2)
    with pytest.raises(ValueError):
        cirq.validate_normalized_state(np.array([1, 1], dtype=np.complex64), 2)
    with pytest.raises(ValueError):
        cirq.validate_normalized_state(
            np.array([1.0, 0.2, 0.0, 0.0], dtype=np.complex64), 2)
    with pytest.raises(ValueError):
        cirq.validate_normalized_state(
            np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64), 2)


def test_sample_state_big_endian():
    results = []
    for x in xrange(8):
        state = cirq.to_valid_state_vector(x, 3)
        sample = cirq.sample_state_vector(state, [2, 1, 0])
        results.append(sample)
    expected = [[list(reversed(x))] for x in
                list(itertools.product([False, True], repeat=3))]
    assert results == expected


def test_sample_state_partial_indices():
    for index in xrange(3):
        for x in xrange(8):
            state = cirq.to_valid_state_vector(x, 3)
            assert (cirq.sample_state_vector(state, [index])
                    == [[bool(1 & (x >> (2 - index)))]])

def test_sample_state_partial_indices_oder():
    for x in xrange(8):
        state = cirq.to_valid_state_vector(x, 3)
        expected = [[bool(1 & (x >> 0)), bool(1 & (x >> 1))]]
        assert cirq.sample_state_vector(state, [2, 1]) == expected


def test_sample_state_partial_indices_all_orders():
    for perm in itertools.permutations([0, 1, 2]):
        for x in xrange(8):
            state = cirq.to_valid_state_vector(x, 3)
            expected = [[bool(1 & (x >> (2 - p))) for p in perm]]
            assert cirq.sample_state_vector(state, perm) == expected


def test_sample_state():
    state = np.zeros(8, dtype=np.complex64)
    state[0] = 1 / np.sqrt(2)
    state[2] = 1 / np.sqrt(2)
    for _ in xrange(10):
        assert cirq.sample_state_vector(state, [2, 1, 0]) in [
            [[False, False, False]],
            [[False, True, False]]]
    # Partial sample is correct.
    for _ in xrange(10):
        assert cirq.sample_state_vector(state, [2]) == [[False]]
        assert cirq.sample_state_vector(state, [0]) == [[False]]


def test_sample_empty_state():
    state = np.array([])
    assert cirq.sample_state_vector(state, []) == [[]]


def test_sample_no_repetitions():
    state = cirq.to_valid_state_vector(0, 3)
    assert cirq.sample_state_vector(state, [1], repetitions=0) == [[]]


def test_sample_state_repetitions():
    for perm in itertools.permutations([0, 1, 2]):
        for x in xrange(8):
            state = cirq.to_valid_state_vector(x, 3)
            expected = [[bool(1 & (x >> (2 - p))) for p in perm]] * 3

            result = cirq.sample_state_vector(state, perm, repetitions=3)
            assert result == expected


def test_sample_state_negative_repetitions():
    state = cirq.to_valid_state_vector(0, 3)
    with pytest.raises(ValueError, match=u'-1'):
        cirq.sample_state_vector(state, [1], repetitions=-1)


def test_sample_state_not_power_of_two():
    with pytest.raises(ValueError, match=u'3'):
        cirq.sample_state_vector(np.array([1, 0, 0]), [1])
    with pytest.raises(ValueError, match=u'5'):
        cirq.sample_state_vector(np.array([0, 1, 0, 0, 0]), [1])


def test_sample_state_index_out_of_range():
    state = cirq.to_valid_state_vector(0, 3)
    with pytest.raises(IndexError, match=u'-2'):
        cirq.sample_state_vector(state, [-2])
    with pytest.raises(IndexError, match=u'3'):
        cirq.sample_state_vector(state, [3])


def test_sample_no_indices():
    state = cirq.to_valid_state_vector(0, 3)
    assert [[]] == cirq.sample_state_vector(state, [])


def test_sample_no_indices_repetitions():
    state = cirq.to_valid_state_vector(0, 3)
    assert [[], []] == cirq.sample_state_vector(state, [], repetitions=2)


def test_measure_state_computational_basis():
    results = []
    for x in xrange(8):
        initial_state = cirq.to_valid_state_vector(x, 3)
        bits, state = cirq.measure_state_vector(initial_state, [2, 1, 0])
        results.append(bits)
        np.testing.assert_almost_equal(state, initial_state)
    expected = [list(reversed(x)) for x in
                list(itertools.product([False, True], repeat=3))]
    assert results == expected


def test_measure_state_reshape():
    results = []
    for x in xrange(8):
        initial_state = np.reshape(cirq.to_valid_state_vector(x, 3), [2] * 3)
        bits, state = cirq.measure_state_vector(initial_state, [2, 1, 0])
        results.append(bits)
        np.testing.assert_almost_equal(state, initial_state)
    expected = [list(reversed(x)) for x in
                list(itertools.product([False, True], repeat=3))]
    assert results == expected


def test_measure_state_partial_indices():
    for index in xrange(3):
        for x in xrange(8):
            initial_state = cirq.to_valid_state_vector(x, 3)
            bits, state = cirq.measure_state_vector(initial_state, [index])
            np.testing.assert_almost_equal(state, initial_state)
            assert bits == [bool(1 & (x >> (2 - index)))]


def test_measure_state_partial_indices_order():
    for x in xrange(8):
        initial_state = cirq.to_valid_state_vector(x, 3)
        bits, state = cirq.measure_state_vector(initial_state, [2, 1])
        np.testing.assert_almost_equal(state, initial_state)
        assert bits == [bool(1 & (x >> 0)), bool(1 & (x >> 1))]


def test_measure_state_partial_indices_all_orders():
    for perm in itertools.permutations([0, 1, 2]):
        for x in xrange(8):
            initial_state = cirq.to_valid_state_vector(x, 3)
            bits, state = cirq.measure_state_vector(initial_state, perm)
            np.testing.assert_almost_equal(state, initial_state)
            assert bits == [bool(1 & (x >> (2 - p))) for p in perm]


def test_measure_state_collapse():
    initial_state = np.zeros(8, dtype=np.complex64)
    initial_state[0] = 1 / np.sqrt(2)
    initial_state[2] = 1 / np.sqrt(2)
    for _ in xrange(10):
        bits, state = cirq.measure_state_vector(initial_state, [2, 1, 0])
        assert bits in [[False, False, False], [False, True, False]]
        expected = np.zeros(8, dtype=np.complex64)
        expected[2 if bits[1] else 0] = 1.0
        np.testing.assert_almost_equal(state, expected)
        assert state is not initial_state

    # Partial sample is correct.
    for _ in xrange(10):
        bits, state = cirq.measure_state_vector(initial_state, [2])
        np.testing.assert_almost_equal(state, initial_state)
        assert bits == [False]

        bits, state = cirq.measure_state_vector(initial_state, [0])
        np.testing.assert_almost_equal(state, initial_state)
        assert bits == [False]


def test_measure_state_out_is_state():
    initial_state = np.zeros(8, dtype=np.complex64)
    initial_state[0] = 1 / np.sqrt(2)
    initial_state[2] = 1 / np.sqrt(2)
    bits, state = cirq.measure_state_vector(initial_state, [2, 1, 0],
                                            out=initial_state)
    expected = np.zeros(8, dtype=np.complex64)
    expected[2 if bits[1] else 0] = 1.0
    np.testing.assert_array_almost_equal(initial_state, expected)
    assert state is initial_state


def test_measure_state_out_is_not_state():
    initial_state = np.zeros(8, dtype=np.complex64)
    initial_state[0] = 1 / np.sqrt(2)
    initial_state[2] = 1 / np.sqrt(2)
    out = np.zeros_like(initial_state)
    _, state = cirq.measure_state_vector(initial_state, [2, 1, 0], out=out)
    assert out is not initial_state
    assert out is state


def test_measure_state_not_power_of_two():
    with pytest.raises(ValueError, match=u'3'):
        _, _ = cirq.measure_state_vector(np.array([1, 0, 0]), [1])
    with pytest.raises(ValueError, match=u'5'):
        cirq.measure_state_vector(np.array([0, 1, 0, 0, 0]), [1])


def test_measure_state_index_out_of_range():
    state = cirq.to_valid_state_vector(0, 3)
    with pytest.raises(IndexError, match=u'-2'):
        cirq.measure_state_vector(state, [-2])
    with pytest.raises(IndexError, match=u'3'):
        cirq.measure_state_vector(state, [3])


def test_measure_state_no_indices():
    initial_state = cirq.to_valid_state_vector(0, 3)
    bits, state = cirq.measure_state_vector(initial_state, [])
    assert [] == bits
    np.testing.assert_almost_equal(state, initial_state)


def test_measure_state_empty_state():
    initial_state = np.array([])
    bits, state = cirq.measure_state_vector(initial_state, [])
    assert [] == bits
    np.testing.assert_almost_equal(state, initial_state)
