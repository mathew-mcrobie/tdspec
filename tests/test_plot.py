import numpy as np

import pytest, tempfile

from pathlib import Path
from tdspec.plot import gaussian, generate_spectrum, plot_spectrum, plot_vlines


@pytest.fixture
def mock_transitions():
    return [
        {"state": 1, "energy_ev": 3.0, "osc_strength": 0.2},
        {"state": 2, "energy_ev": 4.5, "osc_strength": 0.5},
        {"state": 3, "energy_ev": 5.2, "osc_strength": 0.1},
    ]


def test_gaussian_peak_position():
    x = np.linspace(0, 10, 1000)
    mu = 5.0
    fwhm = 1.0
    y = gaussian(x, mu, fwhm)

    max_index = np.argmax(y)
    x_at_max = x[max_index]
    assert abs(x_at_max - mu) < 0.01


def test_gaussian_decay():
    x = np.array([-100, 0, 100])
    y = gaussian(x, mu=0.0, fwhm=1.0)
    assert y[0] < 1e-10
    assert y[2] < 1e-10


def test_gaussian_invalid_fwhm():
    x = np.linspace(0, 10, 100)
    with pytest.raises(ValueError):
        gaussian(x, mu=5.0, fwhm=-1.0)


def test_generate_spectrum_runs(mock_transitions):
    x, y = generate_spectrum(mock_transitions, fwhm=0.3, energy_range=(2.5, 6.0))
    assert x.any() and y.any()


def test_plot_spectrum_creates_file(mock_transitions):
    with tempfile.TemporaryDirectory() as tmpdir:
        outpath = Path(tmpdir) / "spectrum.png"
        x, y = generate_spectrum(mock_transitions, fwhm=0.3, energy_range=(2.5, 6.0))
        plot_spectrum(x, y, filepath=outpath)
        assert outpath.exists()
        assert outpath.stat().st_size > 0


def test_plot_vlines_creates_file(mock_transitions):
    with tempfile.TemporaryDirectory() as tmpdir:
        outpath = Path(tmpdir) / "transitions.png"
        plot_vlines(mock_transitions, outpath=outpath)
        assert outpath.exists()
        assert outpath.stat().st_size > 0

