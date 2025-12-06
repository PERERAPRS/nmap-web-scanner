from flask import Flask, render_template, request
import nmap
import os
from datetime import datetime

app = Flask(__name__)

# Nmap commands based on Image 1 (refer to ![image1](image1))
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
    nm = nmap. PortScanner()

    # Compose the arguments from the scan type
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
                ports = nm[host][proto]. keys()
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
        target = request. form.get("target", "")
        scan_type = request. form.get("scan_type", "")
        extra = request.form.get("extra", "") if scan_type in ("--top-ports", "--script") else ""

        scan_data = scan_target(target, scan_type, extra)
        timestamp = datetime.now(). strftime("%Y-%m-%d %H-%M-%S")

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
    app. run(debug=True)