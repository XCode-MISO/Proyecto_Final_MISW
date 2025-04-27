#!/usr/bin/env python3
"""
Lee coverage.xml (formato Cobertura) y genera un gráfico PNG con
el % global de líneas cubiertas.  Requiere matplotlib + lxml.
"""
import matplotlib.pyplot as plt
from lxml import etree
from pathlib import Path

COV_XML  = Path("coverage.xml")          # generado por pytest-cov
OUT_PNG  = Path("coverage_chart.png")

def main():
    if not COV_XML.exists():
        raise SystemExit("❌ coverage.xml no existe")

    root = etree.parse(COV_XML).getroot()
    pct  = round(float(root.get("line-rate", 0)) * 100, 2)

    covered, uncovered = pct, 100 - pct
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie([covered, uncovered],
           labels=[f"Cubierto {covered:.1f}%", f"No cubierto {uncovered:.1f}%"],
           startangle=90, autopct="%1.1f%%")
    ax.set_title("Cobertura de líneas")
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    print(f"✅  Gráfico generado → {OUT_PNG}")

if __name__ == "__main__":
    main()