"""
Rule-based sustainability scoring built directly from scraped data.
No machine learning involved: each criterion adds or removes points
based on what we discover during scraping.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pandas as pd


@dataclass
class ScoreBreakdown:
    recycled_bonus: float = 0.0
    certifications_bonus: float = 0.0
    supply_chain_bonus: float = 0.0
    labor_bonus: float = 0.0
    environment_bonus: float = 0.0
    unsold_bonus: float = 0.0
    unsold_penalty: float = 0.0
    badge_bonus: float = 0.0

    def total(self) -> float:
        return (
            self.recycled_bonus
            + self.certifications_bonus
            + self.supply_chain_bonus
            + self.labor_bonus
            + self.environment_bonus
            + self.unsold_bonus
            - self.unsold_penalty
            + self.badge_bonus
        )

    def as_dict(self) -> Dict[str, float]:
        return {
            "recycled_bonus": round(self.recycled_bonus, 2),
            "certifications_bonus": round(self.certifications_bonus, 2),
            "supply_chain_bonus": round(self.supply_chain_bonus, 2),
            "labor_bonus": round(self.labor_bonus, 2),
            "environment_bonus": round(self.environment_bonus, 2),
            "unsold_bonus": round(self.unsold_bonus, 2),
            "unsold_penalty": round(self.unsold_penalty, 2),
            "badge_bonus": round(self.badge_bonus, 2),
        }


class SustainabilityScoreCalculator:
    """
    Converts raw scraped signals into a final score between 0 and 10.
    The logic mirrors what an analyst would do manually when reading
    sustainability reports, but automated and consistent for every brand.
    """

    def __init__(self) -> None:
        self.positive_unsold_keywords: List[str] = [
            "donate",
            "charity",
            "recycle",
            "recycling",
            "repair",
            "resale",
            "second hand",
            "zero waste",
            "no destruction",
            "never destroy",
            "upcycle",
            "take back",
            "buyback",
            "circular",
        ]
        self.negative_unsold_keywords: List[str] = [
            "burn",
            "incinerate",
            "destroy",
            "landfill",
        ]

    # ------------------------------------------------------------------ #
    # Public helpers
    # ------------------------------------------------------------------ #
    def score_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns a copy of the dataframe with a `final_score` column
        (rounded to one decimal) and a `score_breakdown` column that
        explains the contribution of each criterion.
        """
        df = df.copy()
        breakdowns: List[Dict[str, float]] = []

        colors: List[Optional[str]] = []

        for idx, row in df.iterrows():
            score, breakdown = self.calculate_score(row)
            df.at[idx, "final_score"] = score
            breakdowns.append(breakdown.as_dict())
            colors.append(score_to_color(score))

        df["score_breakdown"] = breakdowns
        df["score_color"] = colors
        return df

    def calculate_score(self, row: pd.Series) -> Tuple[float, ScoreBreakdown]:
        base_score = 5.0  # neutre : ni bon ni mauvais
        breakdown = ScoreBreakdown()

        # Recycled materials (max +3 points)
        recycled = self._to_float(row.get("sustainable_materials"))
        if recycled is not None:
            bonus = min(recycled / 20.0, 3.0)
            breakdown.recycled_bonus = bonus

        # Certifications (max +2 points)
        cert_count = self._count_entries(row.get("certifications"))
        if cert_count:
            breakdown.certifications_bonus = min(cert_count * 0.5, 2.0)

        # Supply chain transparency (binary +0.5)
        supply_chain_text = self._to_str(row.get("supply_chain_transparency"))
        if supply_chain_text:
            breakdown.supply_chain_bonus = 0.5

        # Labor ethics (max +1.5 points)
        labor_score = self._normalised_ten(row.get("labor_ethics"))
        breakdown.labor_bonus = labor_score * 1.5

        # Environmental impact (max +1.5 points)
        env_score = self._normalised_ten(row.get("global_env_impact"))
        breakdown.environment_bonus = env_score * 1.5

        # Unsold management bonuses / penalties
        unsold_text = self._to_str(row.get("unsold_management"))
        if unsold_text:
            if self._contains(unsold_text, self.positive_unsold_keywords):
                breakdown.unsold_bonus = 1.0
            if self._contains(unsold_text, self.negative_unsold_keywords):
                breakdown.unsold_penalty = 1.5

        # Badges (small boost)
        if self._is_truthy(row.get("planet_badge")):
            breakdown.badge_bonus += 0.5
        if self._is_truthy(row.get("labor_badge")):
            breakdown.badge_bonus += 0.5

        final_score = base_score + breakdown.total()
        final_score = max(0.0, min(10.0, round(final_score, 1)))

        return final_score, breakdown

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _to_float(value: Optional[object]) -> Optional[float]:
        if value is None:
            return None
        try:
            float_value = float(str(value).strip().replace("%", ""))
            return float_value
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _count_entries(text: Optional[object]) -> int:
        if not text:
            return 0
        parts = [part.strip() for part in str(text).split(",")]
        return len([p for p in parts if p])

    @staticmethod
    def _to_str(value: Optional[object]) -> str:
        if value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def _normalised_ten(value: Optional[object]) -> float:
        """
        Converts a score expressed between 0 and 10 into 0-1.
        """
        numeric = SustainabilityScoreCalculator._to_float(value)
        if numeric is None or numeric <= 0:
            return 0.0
        return max(0.0, min(1.0, numeric / 10.0))

    @staticmethod
    def _contains(text: str, keywords: List[str]) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in keywords)

    @staticmethod
    def _is_truthy(value: Optional[object]) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        text = str(value).strip().lower()
        return text not in ("", "0", "false", "none", "['']")


def score_to_color(score: Optional[float]) -> Optional[str]:
    if score is None:
        return None
    if score >= 7.0:
        return "green"
    if score >= 4.0:
        return "orange"
    return "red"


if __name__ == "__main__":
    # Mini test rapide
    df = pd.DataFrame(
        [
            {
                "brand": "Patagonia",
                "sustainable_materials": 87,
                "certifications": "B Corp, Fair Trade",
                "unsold_management": "We donate unsold items and never destroy stock.",
                "supply_chain_transparency": "Detailed supplier list",
                "global_env_impact": 9,
                "labor_ethics": 8,
                "planet_badge": True,
                "labor_badge": True,
            },
            {
                "brand": "FastFashionX",
                "sustainable_materials": 5,
                "certifications": "",
                "unsold_management": "We sometimes burn unsold products.",
                "supply_chain_transparency": "",
                "global_env_impact": 2,
                "labor_ethics": 3,
            },
        ]
    )

    calculator = SustainabilityScoreCalculator()
    scored = calculator.score_dataframe(df)
    print(scored[["brand", "final_score", "score_breakdown"]])

