import pytest
from tdspec.parser import parse_qchem_tddft

MOCK_OUTPUT = """
Standard Output: TDDFT Calculation Begins
Some random junk text here
Excited state 1: excitation energy (eV) =    3.4567
 strength   :    0.1234567

-----------------------
Another banner maybe
Excited state 2: excitation energy (eV) =    4.5678
 strength   :    0.0000000

This line means nothing
Excited state 3: excitation energy (eV) =    5.6789
 strength   :    0.8765432

End of Output
"""

LINES_OUTPUT = [
    "Standard Output: TDDFT Calculation Begins\n",
    "Some random junk text here\n",
    "Excited state 1: excitation energy (eV) =    3.4567\n",
    " strength   :    0.1234567\n",
    "\n",
    "-----------------------\n",
    "Another banner maybe\n",
    "Excited state 2: excitation energy (eV) =    4.5678\n",
    " strength   :    0.0000000\n",
    "\n",
    "This line means nothing\n",
    "Excited state 3: excitation energy (eV) =    5.6789\n",
    " strength   :    0.8765432\n",
    "\n",
    "End of Output",
]


def test_parse_qchem_tddft_basic(tmp_path):
    test_file = tmp_path / "mock_qchem.out"
    test_file.write_text(MOCK_OUTPUT)

    transitions = parse_qchem_tddft(test_file)

    assert len(transitions) == 3
    assert transitions[0]["state"] == 1
    assert transitions[0]["energy_ev"] == pytest.approx(3.4567)
    assert transitions[0]["osc_strength"] == pytest.approx(0.1234567)
    assert transitions[1]["state"] == 2
    assert transitions[1]["energy_ev"] == pytest.approx(4.5678)
    assert transitions[1]["osc_strength"] == pytest.approx(0.0000000)
    assert transitions[2]["state"] == 3
    assert transitions[2]["energy_ev"] == pytest.approx(5.6789)
    assert transitions[2]["osc_strength"] == pytest.approx(0.8765432)

def test_parse_from_lines():
    transitions = parse_qchem_tddft(LINES_OUTPUT)
    assert len(transitions) == 3
    assert transitions[0] == {"state": 1, "energy_ev": 3.4567, "osc_strength": 0.1234567}
    assert transitions[1] == {"state": 2, "energy_ev": 4.5678, "osc_strength": 0.0000000}
    assert transitions[2] == {"state": 3, "energy_ev": 5.6789, "osc_strength": 0.8765432}

