import re


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

