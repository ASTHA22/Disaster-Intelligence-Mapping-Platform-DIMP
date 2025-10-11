import re
from typing import Dict, List, Optional
from datetime import datetime
from transformers import pipeline
import torch

class SocialMediaAnalyzer:
    """NLP-based social media analysis for disaster intelligence"""
    
    def __init__(self):
        # Lazy load sentiment analysis pipeline
        self.sentiment_analyzer = None
        self._model_loaded = False
        
        # Disaster-related keywords
        self.emergency_keywords = {
            "critical": ["help", "urgent", "emergency", "trapped", "injured", "dying", "救命"],
            "damage": ["collapsed", "destroyed", "damaged", "broken", "fire", "explosion"],
            "flood": ["flood", "water", "submerged", "drowning", "overflow", "洪水"],
            "rescue": ["rescue", "evacuate", "shelter", "救援", "避難"],
            "casualty": ["injured", "dead", "casualties", "victims", "missing"]
        }
        
        # Location patterns
        self.location_pattern = re.compile(r'\b(?:at|in|near|from)\s+([A-Z][a-zA-Z\s]+(?:Street|Road|Avenue|City|District|Area|Zone))\b')
    
    def _load_sentiment_model(self):
        """Lazy load sentiment analysis model"""
        if not self._model_loaded:
            try:
                device = 0 if torch.cuda.is_available() else -1
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=device
                )
                self._model_loaded = True
            except Exception as e:
                print(f"Warning: Could not load sentiment model: {e}")
                print("Using keyword-based sentiment analysis")
                self.sentiment_analyzer = None
                self._model_loaded = True
    
    def analyze_post(self, text: str, location: Optional[str] = None, 
                    timestamp: Optional[str] = None) -> Dict:
        """Analyze social media post for disaster intelligence"""
        
        # Extract urgency and category
        urgency, categories = self._classify_urgency(text)
        
        # Extract location if not provided
        if not location:
            location = self._extract_location(text)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(text)
        
        # Extract entities (people, numbers, resources)
        entities = self._extract_entities(text)
        
        # Generate priority score
        priority_score = self._calculate_priority(urgency, categories, sentiment)
        
        return {
            "text": text,
            "urgency": urgency,
            "categories": categories,
            "location": location,
            "sentiment": sentiment,
            "entities": entities,
            "priority_score": priority_score,
            "requires_action": priority_score > 0.7,
            "timestamp": timestamp or datetime.now().isoformat(),
            "recommendations": self._generate_action_items(urgency, categories)
        }
    
    def _classify_urgency(self, text: str) -> tuple:
        """Classify urgency level and disaster categories"""
        text_lower = text.lower()
        categories = []
        urgency_score = 0.0
        
        for category, keywords in self.emergency_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
                if category == "critical":
                    urgency_score = max(urgency_score, 0.9)
                elif category == "casualty":
                    urgency_score = max(urgency_score, 0.85)
                elif category == "rescue":
                    urgency_score = max(urgency_score, 0.8)
                elif category in ["damage", "flood"]:
                    urgency_score = max(urgency_score, 0.6)
        
        # Determine urgency level
        if urgency_score >= 0.8:
            urgency = "critical"
        elif urgency_score >= 0.6:
            urgency = "high"
        elif urgency_score >= 0.4:
            urgency = "medium"
        else:
            urgency = "low"
        
        return urgency, categories
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from text"""
        # Try pattern matching
        match = self.location_pattern.search(text)
        if match:
            return match.group(1).strip()
        
        # Look for capitalized place names
        words = text.split()
        for i, word in enumerate(words):
            if word in ["at", "in", "near", "from"] and i + 1 < len(words):
                if words[i + 1][0].isupper():
                    return " ".join([w for w in words[i+1:i+4] if w[0].isupper()])
        
        return None
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of the post"""
        # Load model if needed
        if not self._model_loaded:
            self._load_sentiment_model()
        
        if self.sentiment_analyzer:
            try:
                result = self.sentiment_analyzer(text[:512])[0]  # Limit text length
                return {
                    "label": result["label"].lower(),
                    "score": float(result["score"])
                }
            except:
                pass
        
        # Fallback: simple keyword-based sentiment
        negative_words = ["help", "emergency", "disaster", "destroyed", "dead", "injured"]
        text_lower = text.lower()
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if negative_count > 2:
            return {"label": "negative", "score": 0.8}
        elif negative_count > 0:
            return {"label": "negative", "score": 0.6}
        else:
            return {"label": "neutral", "score": 0.5}
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract entities like numbers, resources needed"""
        entities = {
            "numbers": [],
            "resources": [],
            "people_count": None
        }
        
        # Extract numbers
        numbers = re.findall(r'\b\d+\b', text)
        entities["numbers"] = [int(n) for n in numbers]
        
        # Extract resource mentions
        resources = ["water", "food", "medicine", "shelter", "blanket", "doctor", "ambulance"]
        text_lower = text.lower()
        entities["resources"] = [r for r in resources if r in text_lower]
        
        # Try to find people count
        people_patterns = [
            r'(\d+)\s+(?:people|persons|individuals|victims)',
            r'(\d+)\s+(?:injured|trapped|missing|dead)'
        ]
        for pattern in people_patterns:
            match = re.search(pattern, text_lower)
            if match:
                entities["people_count"] = int(match.group(1))
                break
        
        return entities
    
    def _calculate_priority(self, urgency: str, categories: List[str], 
                          sentiment: Dict) -> float:
        """Calculate priority score for the post"""
        urgency_scores = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.3}
        base_score = urgency_scores.get(urgency, 0.3)
        
        # Boost for critical categories
        if "critical" in categories or "casualty" in categories:
            base_score = min(base_score + 0.2, 1.0)
        
        # Boost for negative sentiment
        if sentiment["label"] == "negative" and sentiment["score"] > 0.7:
            base_score = min(base_score + 0.1, 1.0)
        
        return round(base_score, 2)
    
    def _generate_action_items(self, urgency: str, categories: List[str]) -> List[str]:
        """Generate recommended actions based on analysis"""
        actions = []
        
        if urgency == "critical":
            actions.append("IMMEDIATE: Dispatch emergency response team")
        
        if "rescue" in categories or "critical" in categories:
            actions.append("Deploy rescue operations")
        
        if "flood" in categories:
            actions.append("Activate water rescue teams")
            actions.append("Prepare evacuation routes")
        
        if "casualty" in categories:
            actions.append("Send medical teams")
            actions.append("Prepare emergency medical supplies")
        
        if "damage" in categories:
            actions.append("Assess structural damage")
            actions.append("Secure perimeter")
        
        return actions if actions else ["Monitor situation"]
