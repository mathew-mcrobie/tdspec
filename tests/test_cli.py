import subprocess

from pathlib import Path


def test_cli_stdout(tmp_path):
    # Create mock .out file
    input_file = tmp_path / "mock_qchem.out"
    input_file.write_text(
        """
        Excited state 1: excitation energy (eV) =    3.4567\n
          strength   :    0.1234567\n
        """
    )

    # Call CLI and capture stdout
    result = subprocess.run(
        ["tdspec", str(input_file)],
        capture_output=True,
        text=True,
        check=True
    )

    assert "State" in result.stdout
    assert "3.457" in result.stdout
    assert "0.1234567" in result.stdout


def test_cli_write_csv(tmp_path):
    input_file = tmp_path / "mock_qchem.out"
    output_file = tmp_path / "results.csv"

    input_file.write_text(
        """
        Excited state 1: excitation energy (eV) =    3.4567\n
          strength   :    0.1234567\n
        """
    )

    subprocess.run(
        ["tdspec", str(input_file), "-o", str(output_file)],
        check=True
    )

    assert output_file.exists()
    contents = output_file.read_text()
    assert "state" in contents
    assert "3.4567" in contents


def test_cli_stdin(tmp_path):
    input_file = tmp_path / "mock_qchem.out"
    input_file.write_text(
        """
        Excited state 1: excitation energy (eV) =    3.4567\n
          strength   :    0.1234567\n
        """
    )

    with input_file.open("rb") as f:
        result = subprocess.run(
            ["tdspec", "-"],
            stdin=f,
            capture_output=True,
            text=True,
            check=True
        )

    assert "State" in result.stdout


def test_cli_plot_style(tmp_path):
    input_file = tmp_path / "mock_qchem.out"
    output_file = tmp_path / "test_plot.png"

    input_file.write_text(
        """
        Excited state 1: excitation energy (eV) =    3.4567\n
          strength   :    0.1234567\n
        """
    )

    with input_file.open("rb") as f:
        result = subprocess.run(
            ["tdspec", str(input_file), "--plot-style", "vlines", "--outplot", str(output_file)],
            check=True
        )

    assert output_file.exists()
