"""
Utilitaires pour calculer la couleur et le label des scores
"""
from typing import Optional


def get_score_color(score: Optional[float]) -> Optional[str]:
    """
    Retourne la couleur associée au score
    """
    if score is None:
        return None
    
    if score >= 8:
        return "green"
    elif score >= 6:
        return "yellow"
    elif score >= 4:
        return "orange"
    else:
        return "red"


def get_score_label(score: Optional[float]) -> Optional[str]:
    """
    Retourne le label associé au score
    """
    if score is None:
        return None
    
    if score >= 8:
        return "Excellent"
    elif score >= 6:
        return "Bon"
    elif score >= 4:
        return "Moyen"
    else:
        return "Faible"


