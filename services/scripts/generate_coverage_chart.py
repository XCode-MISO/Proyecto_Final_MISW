#!/usr/bin/env python3
"""
Script para leer un coverage.xml y generar un gráfico de barras horizontales
con el porcentaje de cobertura por archivo.
Uso:
  python generate_coverage_chart.py <coverage.xml> <output_dir>
"""
import sys
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 3:
        print("Uso: python generate_coverage_chart.py <coverage.xml> <output_dir>")
        sys.exit(1)

    cov_xml_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isfile(cov_xml_path):
        print(f"Error: no se encontró el archivo {cov_xml_path}")
        sys.exit(1)
    if not os.path.isdir(output_dir):
        print(f"Error: el directorio de salida {output_dir} no existe")
        sys.exit(1)

    # Parsear el XML de cobertura
    tree = ET.parse(cov_xml_path)
    root = tree.getroot()

    files = []
    rates = []

    # Cada <class> tiene atributos filename y line-rate (entre 0 y 1)
    for cls in root.findall('.//class'):
        filename = cls.get('filename')
        # Convertir a porcentaje
        line_rate = float(cls.get('line-rate', '0')) * 100
        files.append(filename)
        rates.append(line_rate)

    if not files:
        print("No se encontraron entradas de cobertura en el XML.")
        sys.exit(0)

    # Ordenar por tasa ascendente para mejor legibilidad
    data = sorted(zip(files, rates), key=lambda x: x[1])
    files, rates = zip(*data)

    # Configurar el gráfico
    plt.figure(figsize=(10, max(6, len(files) * 0.3)))
    plt.barh(files, rates)
    plt.xlabel('Cobertura (%)')
    plt.title('Cobertura por archivo')
    plt.tight_layout()

    # Guardar la imagen
    out_path = os.path.join(output_dir, 'coverage_chart.png')
    plt.savefig(out_path)
    print(f"Gráfico guardado en: {out_path}")

if __name__ == '__main__':
    main()
