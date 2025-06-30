import argparse, fileinput, sys

from .parser import parse_qchem_tddft
from .io_utils import write_csv
from pathlib import Path


def main():
    cli_parser = argparse.ArgumentParser(
        description="Extract and process TD-DFT excitation data from quantum chemistry output files"
    )

    # Positional arguments: input file
    cli_parser.add_argument("filepath", type=str, help="Qchem or Gaussian output file to process. '-' to read from stdin")

    # Optional flags
    cli_parser.add_argument("-o", "--output", type=Path, help="Output file for transition data (default: <input>_transitions.csv)")
    cli_parser.add_argument("--format", "--fmt", choices=["csv", "json"], help="Force output format (default: inferred from filename)")
    cli_parser.add_argument("--engine", choices=["qchem", "gaussian"], help="Force parser engine (default: auto-detect)")
    cli_parser.add_argument("--plot", action="store_true", help="Generate a spectrum plot (spectrum.png).")
    cli_parser.add_argument("--fwhm", type=float, default=0.2, help="FWHM for Gaussian broadening (default: 0.2 eV)")
    cli_parser.add_argument("--range", nargs=2, type=float, metavar=("MIN", "MAX"), help="Energy range to plot")
    cli_parser.add_argument("--outplot", type=Path, help="Filename for plot output (default: spectrum.png)")

    args = cli_parser.parse_args()

    try:
        # Parsing
        if args.filepath == "-":
            lines = sys.stdin.read().splitlines()
        else:
            with fileinput.input(files=(args.filepath,)) as f:
                lines = list(f)

        if args.engine == "qchem" or args.engine == None or args.engine == "":
            transitions = parse_qchem_tddft(lines)
        else:
            raise NotImplementedError("Only Q-Chem files are currently supported.")

        # Determine if writing requested.
        if args.output:
            output_path = args.output
            output_format = args.format or output_path.suffix.lstrip(".").lower()

            # Check requested format exists
            if output_format not in {"csv", "json"}:
                raise ValueError(f"Unsupported output format: {output_format}")

            # Write 
            if output_format == "csv":
                write_csv(transitions, outpath=output_path)
            elif output_format == "json":
                write_json(transitions, outpat=output_path)

        if not args.output and not args.plot:
            for t in transitions:
                print(f"State {t['state']:>3}: {t['energy_ev']:6.3f} eV | f = {t['osc_strength']:14.10f}")

        # Plotting
        if args.plot:
            #plot_spectrum()
            raise NotImplementedError
            if args.verbose:
                print(f"Plot written to {args.outplot or 'spectrum.png'}")
           
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)


