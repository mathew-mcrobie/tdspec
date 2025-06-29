#!/usr/bin/env python3

import csv
import sys
import re


def write_csv(transitions, outpath="transitions.csv"):
    with open(outpath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["State", "Energy / eV", "Oscillator Strength"])
        for t in transitions:
            writer.writerow([t["state"], t["energy_ev"], t["osc_strength"]])


def parse_qchem_tddft(filepath):
    transitions = []

    with open(filepath, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        match = re.search(r"Excited state\s+(\d+):.*=\s+(\d+\.\d+(?:[Ee][+-]?\d+)?)", line, re.IGNORECASE)
        if match:
            state = int(match.group(1))
            energy = float(match.group(2))
            osc_strength = None

            for j in range(1, 5):
                if i + j >= len(lines):
                    break
                next_line = lines[i + j]
                osc_match = re.search(r"strength\s*[=:]\s*(\d+\.\d+(?:[Ee][+-]?\d+)?)", next_line, re.IGNORECASE)
                if osc_match:
                    osc_strength = float(osc_match.group(1))
                    break

            transitions.append({
                "state": state,
                "energy_ev": energy,
                "osc_strength": osc_strength,
            })

        i += 1

    return transitions


def main():
    if len(sys.argv) < 2:
        print("Usage: python tdspec.py <output_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        transitions = parse_qchem_tddft(filepath)
        if "-w" in sys.argv:
            write_csv(transitions)
            print("Wrote to transitions.csv")
        else:
            for t in transitions:
                print(f"State {t['state']:>3}: {t['energy_ev']:6.3f} eV | f = {t['osc_strength']:14.10f}")
        
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)

if __name__ == "__main__":
    main()
