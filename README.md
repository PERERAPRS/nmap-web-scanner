# Nmap Web Scanner

A sleek hacker-themed web interface for running powerful Nmap network scans, built with Flask and Python, inspired by retro terminal aesthetics.

![screenshot](screenshot.png)
*Screenshot: see Image 1 for reference.*

---

## Features

- 🖥️ **Terminal-inspired web UI** (see Image 1)
- 🔍 Supports common Nmap scans: Ping, SYN, UDP, Version, OS, Aggressive, etc.
- 💾 Scan result reporting and summary
- 📜 Saves results to a `reports/` directory
- 🧑‍💻 Green-on-black "hacker" theme with monospace fonts, custom CSS, and clean layout

## Demo

![image1](image1)

---

## Installation

### Prerequisites

- Python 3.7+
- [`nmap`](https://nmap.org/) must be installed on your system
- [`python-nmap`](https://pypi.org/project/python-nmap/) (Python bindings)

### Clone the repo

```bash
git clone https://github.com/PERERAPRS/nmap-web-scanner.git
cd nmap-web-scanner
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Manually, you may also need:

```
pip install flask python-nmap
```

### Run Nmap as root if you need special options (like SYN scan).

---

## Usage

```bash
python app.py
```

Then open your browser to [http://localhost:5000](http://localhost:5000)

---

## Scan Types

Supported scan options (as in the UI):

| Name                      | Nmap Option |
|---------------------------|-------------|
| Ping Scan                 | `-sP`       |
| TCP SYN Scan              | `-sS`       |
| UDP Scan                  | `-sU`       |
| Version Detection         | `-sV`       |
| OS Detection              | `-O`        |
| Aggressive Scan           | `-A`        |
| Timing Template           | `-T4`       |
| Input from List           | `-iL`       |
| No Port Scan              | `-sn`       |
| XMAS Scan                 | `-sX`       |
| FIN Scan                  | `-sF`       |
| TCP Connect Scan          | `-sT`       |
| TCP Null Scan             | `-sN`       |
| TCP ACK Scan              | `-sA`       |
| Script Scan (default)     | `-sC`       |

Some options (`--top-ports`, `--script`) will prompt for extra input in the UI.

---

## File Structure

```
.
├── app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── reports/
```

---

## How It Works

1. **User inputs a target** (IP/DNS) and chooses scan type.
2. **Flask app** runs the scan with python-nmap, using selected options.
3. **Results** are displayed in a terminal-style interface and can be found in the `reports` folder.

---

## Example Python Code (app.py)

```python
from flask import Flask, render_template, request
import nmap
import os
from datetime import datetime

app = Flask(__name__)

NMAP_SCAN_OPTIONS = [
    ("Ping Scan", "-sP"),
    ("TCP SYN Scan", "-sS"),
    ("UDP Scan", "-sU"),
    ("Version Detection", "-sV"),
    ("OS Detection", "-O"),
    ("Aggressive Scan", "-A"),
    ("Timing Template", "-T4"),
    ("Input from List", "-iL"),
    ("No Port Scan", "-sn"),
    ("XMAS Scan", "-sX"),
    ("FIN Scan", "-sF"),
    ("TCP Connect Scan", "-sT"),
    ("TCP Null Scan", "-sN"),
    ("TCP ACK Scan", "-sA"),
    ("Script Scan (default scripts)", "-sC")   
]

if not os.path.exists("reports"):
    os.makedirs("reports")


def scan_target(target, scan_type, extra=None):
    nm = nmap.PortScanner()
    arguments = scan_type
    if scan_type == "--top-ports" and extra:
        arguments += f" {extra}"
    if scan_type == "--script" and extra:
        arguments += f" {extra}"

    scan_result = {}
    try:
        nm.scan(target, arguments=arguments)
        for host in nm.all_hosts():
            scan_result[host] = {
                "state": nm[host].state(),
                "protocols": {}
            }
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                scan_result[host]["protocols"][proto] = [
                    {
                        "port": port,
                        "state": nm[host][proto][port]["state"],
                        "name": nm[host][proto][port]["name"],
                        "product": nm[host][proto][port].get("product", "N/A")
                    }
                    for port in ports
                ]
    except Exception as e:
        scan_result["error"] = str(e)

    return scan_result


@app.route("/", methods=["GET", "POST"])
def index():
    scan_data = None
    target = ""
    scan_type = ""
    extra = ""
    timestamp = ""

    if request.method == "POST":
        target = request.form.get("target", "")
        scan_type = request.form.get("scan_type", "")
        extra = request.form.get("extra", "") if scan_type in ("--top-ports", "--script") else ""

        scan_data = scan_target(target, scan_type, extra)
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    return render_template(
        "index.html",
        scan_data=scan_data,
        target=target,
        scan_type=scan_type,
        extra=extra,
        timestamp=timestamp,
        scan_options=NMAP_SCAN_OPTIONS
    )


if __name__ == "__main__":
    app.run(debug=True)
```

---

## Legal

> **Use this tool ONLY on networks you own or have permission to scan. Unauthorized scanning is illegal.**

---

## License

MIT

---
