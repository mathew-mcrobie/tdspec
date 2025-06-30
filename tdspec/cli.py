import argparse, fileinput, sys

from .parser import parse_qchem_tddft
from .io_utils import write_csv
from .plot import generate_spectrum, plot_overlay, plot_spectrum, plot_vlines
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
    cli_parser.add_argument("--plot-style", choices=["spectrum", "vlines", "overlay"], help="Plotting style: 'spectrum' (simulated spectrum), 'vlines' (raw transitions), 'overlay' (both)")
    cli_parser.add_argument("--fwhm", type=float, default=0.2, help="FWHM for Gaussian broadening (default: 0.2 eV)")
    cli_parser.add_argument("--range", nargs=2, type=float, metavar=("MIN", "MAX"), help="Energy range to plot")
    cli_parser.add_argument("--outplot", type=Path, help="Filename for plot output (default: plot.png)")

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
                write_json(transitions, outpath=output_path)

        if not args.output and not args.plot_style:
            for t in transitions:
                print(f"State {t['state']:>3}: {t['energy_ev']:6.3f} eV | f = {t['osc_strength']:14.10f}")

        # Plotting
        if args.plot_style:
            outplot = args.outplot or "plot.png"
            if args.plot_style == "spectrum":
                x, y = generate_spectrum(
                    transitions,
                    fwhm=args.fwhm,
                    energy_range=tuple(args.range) if args.range else None
                )
                plot_spectrum(x, y, filepath=outplot)
                print(f"Plot written to {outplot}")
            elif args.plot_style == "vlines":
                plot_vlines(transitions, outpath=outplot or "transitions.png")
                print(f"Plot written to {outplot}")
            elif args.plot_style == "overlay":
                plot_overlay(transitions, outpath=outplot)
                print(f"Plot written to {outplot}")
           
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)


