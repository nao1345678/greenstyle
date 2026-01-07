"""
Tests unitaires pour score_color.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from utils.score_color import get_score_color, get_score_label


class TestGetScoreColor:
    """Tests pour la fonction get_score_color"""
    
    def test_score_excellent_vert(self):
        """Test que les scores >= 8 retournent 'green'"""
        assert get_score_color(8.0) == "green"
        assert get_score_color(9.5) == "green"
        assert get_score_color(10.0) == "green"
    
    def test_score_bon_jaune(self):
        """Test que les scores entre 6 et 8 retournent 'yellow'"""
        assert get_score_color(6.0) == "yellow"
        assert get_score_color(7.5) == "yellow"
        assert get_score_color(7.99) == "yellow"
    
    def test_score_moyen_orange(self):
        """Test que les scores entre 4 et 6 retournent 'orange'"""
        assert get_score_color(4.0) == "orange"
        assert get_score_color(5.0) == "orange"
        assert get_score_color(5.99) == "orange"
    
    def test_score_faible_rouge(self):
        """Test que les scores < 4 retournent 'red'"""
        assert get_score_color(0.0) == "red"
        assert get_score_color(2.5) == "red"
        assert get_score_color(3.99) == "red"
    
    def test_score_none(self):
        """Test que None retourne None"""
        assert get_score_color(None) is None
    
    def test_scores_limites(self):
        """Test des valeurs limites"""
        assert get_score_color(8.0) == "green"
        assert get_score_color(7.99) == "yellow"
        assert get_score_color(6.0) == "yellow"
        assert get_score_color(5.99) == "orange"
        assert get_score_color(4.0) == "orange"
        assert get_score_color(3.99) == "red"


class TestGetScoreLabel:
    """Tests pour la fonction get_score_label"""
    
    def test_score_excellent(self):
        """Test que les scores >= 8 retournent 'Excellent'"""
        assert get_score_label(8.0) == "Excellent"
        assert get_score_label(9.5) == "Excellent"
        assert get_score_label(10.0) == "Excellent"
    
    def test_score_bon(self):
        """Test que les scores entre 6 et 8 retournent 'Bon'"""
        assert get_score_label(6.0) == "Bon"
        assert get_score_label(7.5) == "Bon"
        assert get_score_label(7.99) == "Bon"
    
    def test_score_moyen(self):
        """Test que les scores entre 4 et 6 retournent 'Moyen'"""
        assert get_score_label(4.0) == "Moyen"
        assert get_score_label(5.0) == "Moyen"
        assert get_score_label(5.99) == "Moyen"
    
    def test_score_faible(self):
        """Test que les scores < 4 retournent 'Faible'"""
        assert get_score_label(0.0) == "Faible"
        assert get_score_label(2.5) == "Faible"
        assert get_score_label(3.99) == "Faible"
    
    def test_score_none(self):
        """Test que None retourne None"""
        assert get_score_label(None) is None
    
    def test_scores_limites(self):
        """Test des valeurs limites"""
        assert get_score_label(8.0) == "Excellent"
        assert get_score_label(7.99) == "Bon"
        assert get_score_label(6.0) == "Bon"
        assert get_score_label(5.99) == "Moyen"
        assert get_score_label(4.0) == "Moyen"
        assert get_score_label(3.99) == "Faible"

