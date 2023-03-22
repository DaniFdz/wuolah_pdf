# Wuolah pdf
Remove the ads and merge pdf's from wuolah

## Installation

Clone the repository
```bash
git clone https://github.com/DaniFdz/wuolah-pdf.git
cd wuolah_pdf
```

Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the requirements
```bash
pip install -r requirements.txt
```

Give the script execution permissions
```bash
chmod +x wuolah_pdf.py
```

## Usage

```
wuolah_pdf.py [-h] [-o OUTPUT] [-r] [-v] [-l] input [input ...]

This program will merge the pdf files that you pass as arguments into one file and will remove the ads from the pdf if you want to

positional arguments:
  input                 Input file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name, if not specified it will be the name of the first file with _merged.pdf at the end
  -r, --remove-ads      Remove the ads from the pdf
  -v, --verbose         Verbose mode, show more info about the process
  -l, --log             File to save the logs of the operations
```

