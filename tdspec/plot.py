import matplotlib.pyplot as plt
import numpy as np


def gaussian(x, mu, fwhm):
    if fwhm < 0.0:
        raise ValueError("FWHM must be positive.")

    sigma = fwhm / (2 * (2 * np.log(2)) ** 0.5)
    return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def generate_spectrum(transitions, fwhm=0.5, energy_range=None, resolution=1000):
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


def plot_vlines(transitions, outpath="transitions.png", energy_range=None):
    energies = [t["energy_ev"] for t in transitions]
    strengths = [t["osc_strength"] for t in transitions]

    plt.vlines(energies, [0], strengths, colors="red", linewidth=2.0)
    if energy_range:
        e_min, e_max = energy_range
        plt.xlim(e_min, e_max)
    plt.ylim(bottom=0)
    plt.xlabel("Energy / eV")
    plt.ylabel("Oscillator Strength")
    plt.title("TD-DFT Transitions")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_spectrum(x, y, filepath="spectrum.png", energy_range=None):
    plt.figure()
    plt.plot(x, y, color="black")
    if energy_range:
        e_min, e_max = energy_range
        plt.xlim(e_min, e_max)
    plt.ylim(bottom=0)
    plt.xlabel("Energy / eV")
    plt.ylabel("Intensity / a.u.")
    plt.title("Simulated TD-DFT Spectrum")
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()


def plot_overlay(transitions, outpath="spectrum.png", fwhm=0.5, energy_range=None, resolution=1000):
    if not transitions:
        raise ValueError("No transitions provided")

    energies = np.array([t["energy_ev"] for t in transitions])
    strengths = np.array([t["osc_strength"] for t in transitions])

    x, y = generate_spectrum(transitions, fwhm=fwhm, energy_range=energy_range, resolution=resolution)

    plt.figure()
    plt.vlines(energies, [0], strengths, color="red", alpha=0.6, linewidth=2, label="Transitions")
    plt.plot(x, y, color="black", label="Broadened Spectrum")
    plt.xlabel("Energy / eV")
    plt.ylabel("Oscillator Strength")
    if energy_range:
        e_min, e_max = energy_range
        plt.xlim(e_min, e_max)
    plt.ylim(bottom=0)
    plt.title("TD-DFT Spectrum Overlay")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

