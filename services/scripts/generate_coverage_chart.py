#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) != 3:
        print("Usage: generate_coverage_chart.py <coverage.xml> <output.png>")
        sys.exit(1)

    xml_path, out_path = sys.argv[1], sys.argv[2]

    # Parse cobertura XML
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML '{xml_path}': {e}")
        sys.exit(1)

    # Extract overall line-rate
    line_rate = float(root.attrib.get('line-rate', 0))
    percent = line_rate * 100

    # Ensure output directory exists
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Create bar chart
    plt.figure(figsize=(4, 6))
    plt.bar(['Coverage'], [percent])
    plt.ylabel('Coverage (%)')
    plt.ylim(0, 100)
    plt.title('Test Coverage')
    plt.tight_layout()

    # Save the chart
    try:
        plt.savefig(out_path)
        print(f"Coverage chart saved to {out_path}")
    except Exception as e:
        print(f"Error saving chart '{out_path}': {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
