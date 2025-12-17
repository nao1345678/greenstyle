"""
Utilitaire pour convertir un score de durabilité en couleur
"""


def get_score_color(score: float) -> str:
    """
    Convertit un score de durabilité (0-10) en couleur
    
    Args:
        score: Score de durabilité entre 0 et 10
        
    Returns:
        Couleur hexadécimale (vert, orange, rouge)
    """
    if score is None:
        return "#808080"  # Gris si pas de score
    
    # Normaliser le score entre 0 et 10
    normalized_score = max(0, min(10, float(score)))
    
    # Vert: 7-10 (excellent)
    if normalized_score >= 7:
        return "#22c55e"  # Vert
    
    # Orange: 4-6.9 (moyen)
    elif normalized_score >= 4:
        return "#f59e0b"  # Orange
    
    # Rouge: 0-3.9 (faible)
    else:
        return "#ef4444"  # Rouge


def get_score_label(score: float) -> str:
    """
    Retourne un label textuel pour le score
    
    Args:
        score: Score de durabilité entre 0 et 10
        
    Returns:
        Label: "Excellent", "Bon", "Moyen", "Faible"
    """
    if score is None:
        return "Non évalué"
    
    normalized_score = max(0, min(10, float(score)))
    
    if normalized_score >= 8:
        return "Excellent"
    elif normalized_score >= 6:
        return "Bon"
    elif normalized_score >= 4:
        return "Moyen"
    else:
        return "Faible"

