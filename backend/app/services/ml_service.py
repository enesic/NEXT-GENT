"""
ML Service for Intent Classification and Response Generation
Uses TF-IDF similarity matching for intent detection
"""
import json
import os
import random
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

class MLService:
    """
    Simple ML service for helpdesk chatbot.
    Uses TF-IDF-like similarity matching for intent classification.
    """
    
    def __init__(self):
        self.training_data = None
        self.intents = []
        self._load_training_data()
    
    def _load_training_data(self):
        """Load training data from JSON file."""
        try:
            data_path = Path(__file__).parent / "ml_training_data.json"
            with open(data_path, 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
                self.intents = self.training_data.get('intents', [])
        except Exception as e:
            print(f"Error loading training data: {e}")
            self.training_data = {"intents": [], "fallback_responses": []}
            self.intents = []
    
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text for matching.
        Converts to lowercase, removes punctuation, splits into words.
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove common Turkish stop words
        stop_words = {'ve', 'veya', 'ile', 'için', 'bir', 'bu', 'şu', 'o', 'ne', 'nasıl', 
                     'nedir', 'mi', 'mı', 'mu', 'mü', 'the', 'a', 'an', 'is', 'are', 'what'}
        words = [w for w in words if w not in stop_words and len(w) > 1]
        
        return words
    
    def _calculate_similarity(self, text_words: List[str], example_words: List[str]) -> float:
        """
        Calculate similarity between two word lists.
        Simple word overlap ratio.
        """
        if not text_words or not example_words:
            return 0.0
        
        # Count matching words
        matches = sum(1 for word in text_words if word in example_words)
        
        # Calculate similarity as ratio of matches to total unique words
        total_unique = len(set(text_words + example_words))
        similarity = matches / total_unique if total_unique > 0 else 0.0
        
        return similarity
    
    def classify_intent(self, message: str, threshold: float = 0.15) -> Tuple[Optional[str], float]:
        """
        Classify intent of user message.
        
        Args:
            message: User message
            threshold: Minimum similarity threshold (default 0.15)
        
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        message_words = self._preprocess_text(message)
        
        best_intent = None
        best_score = 0.0
        
        for intent_data in self.intents:
            intent_name = intent_data.get('intent')
            examples = intent_data.get('examples', [])
            
            # Calculate similarity with each example
            max_similarity = 0.0
            for example in examples:
                example_words = self._preprocess_text(example)
                similarity = self._calculate_similarity(message_words, example_words)
                max_similarity = max(max_similarity, similarity)
            
            # Update best match
            if max_similarity > best_score:
                best_score = max_similarity
                best_intent = intent_name
        
        # Return None if below threshold
        if best_score < threshold:
            return None, 0.0
        
        return best_intent, best_score
    
    def get_response(self, intent: str) -> str:
        """
        Get response for a given intent.
        
        Args:
            intent: Intent name
        
        Returns:
            Response text
        """
        for intent_data in self.intents:
            if intent_data.get('intent') == intent:
                responses = intent_data.get('responses', [])
                if responses:
                    return random.choice(responses)
        
        # Fallback response
        fallback_responses = self.training_data.get('fallback_responses', [])
        if fallback_responses:
            return random.choice(fallback_responses)
        
        return "Üzgünüm, size yardımcı olamıyorum. Lütfen support@nextgent.com ile iletişime geçin."
    
    def get_fallback_response(self) -> str:
        """Get a random fallback response."""
        fallback_responses = self.training_data.get('fallback_responses', [])
        if fallback_responses:
            return random.choice(fallback_responses)
        return "Üzgünüm, size yardımcı olamıyorum. Lütfen support@nextgent.com ile iletişime geçin."
    
    def process_message(self, message: str) -> Dict[str, any]:
        """
        Process user message and return response.
        
        Args:
            message: User message
        
        Returns:
            Dict with intent, confidence, and response
        """
        intent, confidence = self.classify_intent(message)
        
        if intent:
            response = self.get_response(intent)
        else:
            intent = "unknown"
            response = self.get_fallback_response()
        
        return {
            "intent": intent,
            "confidence": confidence,
            "response": response,
            "suggestions": self._get_suggestions(intent)
        }
    
    def _get_suggestions(self, intent: Optional[str]) -> List[str]:
        """Get suggested follow-up questions based on intent."""
        suggestions_map = {
            "pricing_inquiry": [
                "Özellikler neler?",
                "Demo görmek istiyorum",
                "Entegrasyon desteği var mı?"
            ],
            "features_inquiry": [
                "Fiyatlandırma nasıl?",
                "Güvenlik özellikleri neler?",
                "Demo talep et"
            ],
            "appointment_help": [
                "Randevu nasıl iptal edilir?",
                "Toplu randevu oluşturma",
                "Randevu bildirimleri"
            ],
            "technical_support": [
                "Dokümantasyon",
                "Video rehberler",
                "Canlı destek saatleri"
            ],
            "demo_request": [
                "Ücretsiz deneme süresi",
                "Demo randevusu al",
                "Özellikler hakkında bilgi"
            ],
            "unknown": [
                "Fiyatlandırma bilgisi",
                "Özellikler hakkında bilgi",
                "Demo talep et"
            ]
        }
        
        return suggestions_map.get(intent, suggestions_map["unknown"])


# Singleton instance
_ml_service_instance = None

def get_ml_service() -> MLService:
    """Get singleton ML service instance."""
    global _ml_service_instance
    if _ml_service_instance is None:
        _ml_service_instance = MLService()
    return _ml_service_instance
