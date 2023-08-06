import json

import progressbar

from .data_acquisition import DataAcquisition


__all__ = ["DataAcquisition", "main", "__version__", "__author__"]
__version__ = "0.1.0"
__author__ = "Oprax <oprax@me.com>"


def main():
    da = DataAcquisition(ns=("9.9.9.9", "80.67.169.12", "80.67.169.40"))
    domains = []
    with open("./domains.txt", "r") as f:
        for domain in f:
            domain = domain.strip()
            if not domain.endswith("."):
                domain += "."
            domains.append(domain)
    alls = {}
    for domain in progressbar.progressbar(domains):
        alls[domain] = da.run(domain)
    with open("./results.json", "w") as f:
        f.write(json.dumps(alls, indent=4))
