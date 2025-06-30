from tdspec.io_utils import write_csv
import csv

def test_write_csv_creates_expected_file(tmp_path):
    transitions = [
        {"state": 1, "energy_ev": 3.4567, "osc_strength": 0.1234567},
        {"state": 2, "energy_ev": 4.5678, "osc_strength": 0.0000000},
        {"state": 3, "energy_ev": 5.6789, "osc_strength": 0.8765432},
    ]

    outfile = tmp_path / "test.csv"
    write_csv(transitions, outpath=outfile)

    with open(outfile, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 3
    assert rows[0]["state"] == "1"
    assert rows[0]["energy_ev"] == "3.4567"
    assert rows[0]["osc_strength"] == "0.1234567"
    assert rows[1]["state"] == "2"
    assert rows[1]["energy_ev"] == "4.5678"
    assert rows[1]["osc_strength"] == "0.0000000"
    assert rows[2]["state"] == "3"
    assert rows[2]["energy_ev"] == "5.6789"
    assert rows[2]["osc_strength"] == "0.8765432"

