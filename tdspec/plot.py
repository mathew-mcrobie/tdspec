import matplotlib.pyplot as plt
import numpy as np


def gaussian(x, mu, fwhm):
    if fwhm < 0.0:
        raise ValueError("FWHM must be positive.")

    sigma = fwhm / (2 * (2 * np.log(2)) ** 0.5)
    return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def plot_vlines(transitions, outpath="transitions.png"):
    energies = [t["energy_ev"] for t in transitions]
    strengths = [t["osc_strength"] for t in transitions]

    plt.vlines(energies, [0], strengths, colors="red", linewidth=2.0)
    plt.xlabel("Energy / eV")
    plt.ylabel("Oscillator Strength")
    plt.title("TD-DFT Transitions")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def generate_spectrum(transitions, fwhm=0.2, energy_range=None, resolution=1000):
    if not transitions:
        raise ValueError("No transitions provided")

    min_e = min(t['energy_ev'] for t in transitions)
    max_e = max(t['energy_ev'] for t in transitions)

    if energy_range:
        min_e, max_e = energy_range
    else:
        margin = fwhm * 2
        min_e -= margin
        max_e += margin

    x = np.linspace(min_e, max_e, resolution)
    y = np.zeros_like(x)

    for t in transitions:
        y += t['osc_strength'] * gaussian(x, t['energy_ev'], fwhm)

    return x, y


def plot_spectrum(x, y, filepath="spectrum.png"):
    plt.figure()
    plt.plot(x, y, color="black")
    plt.xlabel("Energy / eV")
    plt.ylabel("Intensity / a.u.")
    plt.title("Simulated TD-DFT Spectrum")
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
