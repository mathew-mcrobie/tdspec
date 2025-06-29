from .parser import parse_qchem_tddft
from .io_utils import write_csv


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

