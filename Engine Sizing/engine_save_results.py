import csv
import numpy as np
from datetime import datetime
from pathlib import Path


def flatten_dictionary(dictionary, parent_key=""):
    """Flatten nested dictionaries into dotted key names."""
    flattened = {}

    for key, value in dictionary.items():
        new_key = f"{parent_key}.{key}" if parent_key else str(key)

        if isinstance(value, dict):
            flattened.update(flatten_dictionary(value, new_key))
        elif isinstance(value, (list, tuple, np.ndarray)):
            flattened[new_key] = str(value)
        elif isinstance(value, np.generic):
            flattened[new_key] = value.item()
        else:
            flattened[new_key] = value

    return flattened


def save_results(
    inputs,
    results,
    filename_prefix="CPL_design"
):
    """Save inputs and results to a timestamped CSV."""

    # Save under the current user's home directory
    output_folder = Path.home() / "CPL" / "CPL Engine Designs"

    # Create folders if they do not already exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"

    # Full output path
    filepath = output_folder / filename

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["CPL Engine Design Results"])
        writer.writerow(["Generated", datetime.now().isoformat()])
        writer.writerow([])

        # Write inputs
        writer.writerow(["INPUTS"])
        writer.writerow(["Parameter", "Value"])

        for key, value in flatten_dictionary(inputs).items():
            writer.writerow([key, value])

        writer.writerow([])

        # Write results
        for section, section_data in results.items():
            writer.writerow([section])
            writer.writerow(["Parameter", "Value"])

            if isinstance(section_data, dict):
                for key, value in flatten_dictionary(section_data).items():
                    writer.writerow([key, value])
            else:
                writer.writerow(["Value", section_data])

            writer.writerow([])

    print(f"Results saved to: {filepath}")

    return str(filepath)