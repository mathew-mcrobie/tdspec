import csv


def write_csv(transitions, outpath="transitions.csv"):
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["state", "energy_ev", "osc_strength"])
        writer.writeheader()

        
        for t in transitions:
            writer.writerow({
                "state": t["state"],
                "energy_ev": f"{t['energy_ev']:.4f}",
                "osc_strength": f"{t['osc_strength']:.7f}",
            })

