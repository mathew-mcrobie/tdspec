import csv


def write_csv(transitions, outpath="transitions.csv"):
    with open(outpath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["State", "Energy / eV", "Oscillator Strength"])
        for t in transitions:
            writer.writerow([t["state"], t["energy_ev"], t["osc_strength"]])


