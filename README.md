# tdspec - a small tool for parsing and analysing tddft logfiles

## Installation

tdspec can be downloaded and installed via git clone.
```bash
git clone https://github.com/mathew-mcrobie/tdspec.git
```

To install it I recommend `cd`ing into the tdspec directory and using pip.
```bash
pip install .
```
If your system requires you to activate a virtual environment, be sure to do that first
```bash
python -m venv .venv --upgrade-deps
source .venv/bin/activate
```

These instructions may be slightly different for windows systems. Full details for how to make and activate virtual environments can be found in the [official Python documentation](https://docs.python.org/3/library/venv.html)

## Usage
A full list of options and usage information can be found via `tdspec --help`
```bash
tdspec --help

usage: tdspec [-h] [-o OUTPUT] [--format {csv,json}] [--engine {qchem,gaussian}]
              [--plot-style {spectrum,vlines,overlay}] [--fwhm FWHM] [--range MIN MAX]
              [--outplot OUTPLOT]
              filepath

Extract and process TD-DFT excitation data from quantum chemistry output files

positional arguments:
  filepath              Qchem or Gaussian output file to process. '-' to read from stdin

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Output file for transition data (default: <input>_transitions.csv)
  --format, --fmt {csv,json}
                        Force output format (default: inferred from filename)
  --engine {qchem,gaussian}
                        Force parser engine (default: auto-detect)
  --plot-style {spectrum,vlines,overlay}
                        Plotting style: 'spectrum' (simulated spectrum), 'vlines' (raw
                        transitions), 'overlay' (both)
  --fwhm FWHM           FWHM for Gaussian broadening (default: 0.2 eV)
  --range MIN MAX       Energy range to plot
  --outplot OUTPLOT     Filename for plot output (default: plot.png)
```

tdspec is built with UNIX composition in mind. By default it will output to `stdout`, but this can be changed with the `-o` option to specify an output file. Alternatively use redirects:
```bash
tdspec qchemoutput.out | grep 'excitation [1-5]' > transitions.csv
```

By specifying an output plot destination via `--outplot` one can create vline spectra for all transitions, generate simulated spectra via gaussian broadening, and show the two overlayed. This behaviour can be controlled by the --plot-style flag. 

## License
[MIT](https://opensource.org/license/MIT)
