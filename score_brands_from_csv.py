#!/usr/bin/env python3
"""
Utility script to turn a raw scraped CSV into a scored dataset.

Usage:
    python score_brands_from_csv.py --input brands_database_with_recycled_materials.csv \
        --output brands_scored.csv
"""

import argparse
from pathlib import Path

import pandas as pd

from sustainability_score_calculator import (
    SustainabilityScoreCalculator,
    score_to_color,
)


def score_file(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    df = pd.read_csv(input_path)

    calculator = SustainabilityScoreCalculator()
    scored_df = calculator.score_dataframe(df)

    # Ensure columns are present even if some brands have missing data
    if "score_color" not in scored_df.columns:
        scored_df["score_color"] = scored_df["final_score"].apply(score_to_color)

    scored_df.to_csv(output_path, index=False)
    print(f"Saved scored dataset to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compute rule-based sustainability scores from a scraped CSV."
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="Path to the scraped CSV file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
        help="Path where the scored CSV will be saved.",
    )
    args = parser.parse_args()
    score_file(args.input, args.output)


if __name__ == "__main__":
    main()


