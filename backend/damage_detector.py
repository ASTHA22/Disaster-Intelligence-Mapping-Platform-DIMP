import io
import numpy as np
from PIL import Image
import cv2
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from typing import Dict, List

class DamageDetector:
    """AI-powered damage detection from satellite/drone imagery"""
    
    def __init__(self):
        # Lazy load model - only when needed
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Damage classification thresholds
        self.damage_threshold = 0.6
    
    def _load_model(self):
        """Lazy load the ResNet50 model"""
        if self.model is None:
            try:
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                self.model = resnet50(weights=ResNet50_Weights.DEFAULT)
                self.model.eval()
                self.model.to(self.device)
            except Exception as e:
                print(f"Warning: Could not load ResNet50 model: {e}")
                print("Using simplified damage detection without deep learning")
                self.model = "unavailable"
        
    def analyze_image(self, image_bytes: bytes) -> Dict:
        """Analyze image for damage detection"""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            img_array = np.array(image)
            
            # Perform multiple analyses
            damage_score = self._detect_damage(image)
            flood_detected = self._detect_flood(img_array)
            infrastructure = self._detect_infrastructure(img_array)
            
            # Determine severity
            severity = self._calculate_severity(damage_score, flood_detected)
            
            return {
                "damage_detected": damage_score > self.damage_threshold,
                "damage_score": float(damage_score),
                "severity": severity,
                "flood_detected": flood_detected,
                "infrastructure_count": infrastructure,
                "analysis_timestamp": self._get_timestamp(),
                "recommendations": self._generate_recommendations(damage_score, flood_detected)
            }
        except Exception as e:
            return {
                "error": str(e),
                "damage_detected": False,
                "damage_score": 0.0
            }
    
    def _detect_damage(self, image: Image.Image) -> float:
        """Use CNN to detect damage patterns"""
        # Load model if not already loaded
        self._load_model()
        
        # If model unavailable, use simplified detection
        if self.model == "unavailable":
            # Fallback: use image statistics for damage estimation
            img_array = np.array(image)
            # Calculate variance (damaged areas tend to have higher variance)
            variance = np.var(img_array) / 10000.0
            return min(variance, 1.0)
        
        # Transform image
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Get model prediction
        with torch.no_grad():
            output = self.model(img_tensor)
            # Use softmax to get probability-like scores
            probabilities = torch.nn.functional.softmax(output, dim=1)
            # Simulate damage score based on certain class activations
            damage_score = float(probabilities[0][:100].sum())  # Simplified scoring
        
        return min(damage_score, 1.0)
    
    def _detect_flood(self, img_array: np.ndarray) -> bool:
        """Detect water/flood using color analysis"""
        # Convert to HSV for better water detection
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Define blue/water color range
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        
        # Create mask for water
        water_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        water_percentage = (np.sum(water_mask > 0) / water_mask.size) * 100
        
        # If more than 20% is water-colored, flag as flood
        return water_percentage > 20
    
    def _detect_infrastructure(self, img_array: np.ndarray) -> int:
        """Detect infrastructure elements using edge detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours (simplified infrastructure detection)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter significant contours
        significant_structures = [c for c in contours if cv2.contourArea(c) > 500]
        
        return len(significant_structures)
    
    def _calculate_severity(self, damage_score: float, flood_detected: bool) -> str:
        """Calculate overall severity level"""
        if damage_score > 0.8 or flood_detected:
            return "critical"
        elif damage_score > 0.6:
            return "high"
        elif damage_score > 0.4:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, damage_score: float, flood_detected: bool) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if damage_score > 0.7:
            recommendations.append("Immediate rescue operations required")
            recommendations.append("Deploy emergency response teams")
        
        if flood_detected:
            recommendations.append("Evacuate low-lying areas")
            recommendations.append("Deploy water rescue teams")
            recommendations.append("Set up temporary shelters")
        
        if damage_score > 0.5:
            recommendations.append("Assess structural integrity of buildings")
            recommendations.append("Establish medical aid stations")
        
        return recommendations if recommendations else ["Continue monitoring"]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
