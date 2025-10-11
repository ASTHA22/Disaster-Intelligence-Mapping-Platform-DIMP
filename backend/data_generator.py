import random
from datetime import datetime, timedelta
from typing import List, Dict

class DataGenerator:
    """Generate realistic sample data for disaster scenarios"""
    
    def __init__(self, location="mumbai"):
        # Sample coordinates - can be set to user's location
        if location.lower() == "mumbai":
            self.base_lat = 19.0760  # Mumbai
            self.base_lon = 72.8777
            self.locations = [
                "Colaba", "Bandra", "Andheri", "Juhu", "Worli",
                "Dadar", "Kurla", "Powai", "Goregaon", "Malad",
                "Borivali", "Kandivali", "Santacruz", "Vile Parle", "Churchgate"
            ]
        else:  # Default Delhi
            self.base_lat = 28.6139
            self.base_lon = 77.2090
            self.locations = [
                "Connaught Place", "Karol Bagh", "Dwarka", "Rohini", "Saket",
                "Nehru Place", "Lajpat Nagar", "Vasant Kunj", "Mayur Vihar",
                "Janakpuri", "Pitampura", "Rajouri Garden", "Shahdara"
            ]
        
    def generate_disaster_zones(self) -> List[Dict]:
        """Generate disaster zone data"""
        zones = []
        for i in range(15):
            zone = {
                "id": f"zone_{i+1}",
                "name": random.choice(self.locations),
                "coordinates": {
                    "lat": self.base_lat + random.uniform(-0.1, 0.1),
                    "lon": self.base_lon + random.uniform(-0.1, 0.1)
                },
                "severity": random.choice(["critical", "high", "medium", "low"]),
                "damage_score": round(random.uniform(0.3, 1.0), 2),
                "affected_area_km2": round(random.uniform(5, 50), 1),
                "last_updated": self._random_timestamp()
            }
            zones.append(zone)
        return zones
    
    def generate_flood_areas(self) -> List[Dict]:
        """Generate flood-affected areas"""
        flood_areas = []
        for i in range(8):
            area = {
                "id": f"flood_{i+1}",
                "location": random.choice(self.locations),
                "coordinates": {
                    "lat": self.base_lat + random.uniform(-0.08, 0.08),
                    "lon": self.base_lon + random.uniform(-0.08, 0.08)
                },
                "water_level_m": round(random.uniform(0.5, 3.5), 1),
                "affected_population": random.randint(500, 5000),
                "status": random.choice(["rising", "stable", "receding"]),
                "evacuation_required": random.choice([True, False]),
                "timestamp": self._random_timestamp()
            }
            flood_areas.append(area)
        return flood_areas
    
    def generate_infrastructure_damage(self) -> List[Dict]:
        """Generate damaged infrastructure data"""
        infrastructure_types = ["bridge", "road", "building", "hospital", "school", "power_station"]
        infrastructure = []
        
        for i in range(20):
            item = {
                "id": f"infra_{i+1}",
                "type": random.choice(infrastructure_types),
                "name": f"{random.choice(self.locations)} {random.choice(infrastructure_types).title()}",
                "coordinates": {
                    "lat": self.base_lat + random.uniform(-0.12, 0.12),
                    "lon": self.base_lon + random.uniform(-0.12, 0.12)
                },
                "damage_level": random.choice(["destroyed", "severe", "moderate", "minor"]),
                "operational": random.choice([True, False]),
                "priority": random.choice(["critical", "high", "medium", "low"]),
                "estimated_repair_days": random.randint(1, 90),
                "timestamp": self._random_timestamp()
            }
            infrastructure.append(item)
        return infrastructure
    
    def generate_displacement_data(self) -> List[Dict]:
        """Generate population displacement data"""
        displacement = []
        for i in range(10):
            zone = {
                "id": f"displacement_{i+1}",
                "area": random.choice(self.locations),
                "coordinates": {
                    "lat": self.base_lat + random.uniform(-0.1, 0.1),
                    "lon": self.base_lon + random.uniform(-0.1, 0.1)
                },
                "displaced_count": random.randint(100, 3000),
                "shelter_capacity": random.randint(50, 2000),
                "needs": random.sample(["food", "water", "medicine", "blankets", "tents"], k=3),
                "status": random.choice(["critical", "stable", "improving"]),
            }
            displacement.append(zone)
        return displacement
    
    def generate_social_feed(self) -> List[Dict]:
        """Generate social media posts"""
        # Mumbai-specific posts
        mumbai_posts = [
            "Urgent! Building collapsed at Colaba. Multiple people trapped. Need immediate help! #MumbaiDisaster",
            "Severe flooding in Bandra area. Water level rising rapidly. Evacuate immediately!",
            "Road to JJ Hospital completely blocked. Ambulances cannot pass. #Emergency",
            "Andheri market area under 3 feet water. Shopkeepers requesting rescue.",
            "Power outage in entire Juhu sector. Backup generators needed for hospitals.",
            "Worli sea link access flooded. Services suspended. Thousands stranded.",
            "Dadar residents trapped on rooftops. Helicopter rescue needed urgently.",
            "Kurla school building showing cracks. Children evacuated safely.",
            "Fire outbreak in Powai due to gas leak. Fire brigade required ASAP.",
            "Goregaon hospital damaged. Patients being moved to temporary facility.",
            "Clean drinking water needed in Malad. Contamination risk high.",
            "Borivali school converted to shelter. Need blankets and food supplies.",
            "Kandivali area completely submerged. Boat rescue operations needed.",
            "Multiple casualties reported in Santacruz. Medical teams required.",
            "Communication lines down in Vile Parle. Unable to reach emergency services."
        ]
        
        # Delhi-specific posts (fallback)
        delhi_posts = [
            "Urgent! Building collapsed at Connaught Place. Multiple people trapped. Need immediate help! #DelhiDisaster",
            "Severe flooding in Yamuna River area. Water level rising rapidly. Evacuate immediately!",
            "Road to AIIMS completely blocked due to fallen tree. Ambulances cannot pass. #Emergency",
            "Karol Bagh market area under 3 feet water. Shopkeepers requesting rescue.",
            "Power outage in entire Dwarka sector. Backup generators needed for hospitals.",
            "Nehru Place metro station flooded. Services suspended. Thousands stranded.",
            "Lajpat Nagar residents trapped on rooftops. Helicopter rescue needed urgently.",
            "Vasant Kunj school building showing cracks. Children evacuated safely.",
            "Fire outbreak in Mayur Vihar due to gas leak. Fire brigade required ASAP.",
            "Janakpuri hospital damaged. Patients being moved to temporary facility.",
            "Clean drinking water needed in Pitampura. Contamination risk high.",
            "Rajouri Garden school converted to shelter. Need blankets and food supplies.",
            "Shahdara area completely submerged. Boat rescue operations needed.",
            "Multiple casualties reported in Dwarka sector 10. Medical teams required.",
            "Communication lines down in Rohini. Unable to reach emergency services."
        ]
        
        # Use Mumbai posts if base_lat is Mumbai, else Delhi
        sample_posts = mumbai_posts if self.base_lat < 20 else delhi_posts
        
        feed = []
        for i, post_text in enumerate(sample_posts):
            post = {
                "id": f"post_{i+1}",
                "text": post_text,
                "location": random.choice(self.locations),
                "coordinates": {
                    "lat": self.base_lat + random.uniform(-0.1, 0.1),
                    "lon": self.base_lon + random.uniform(-0.1, 0.1)
                },
                "urgency": random.choice(["critical", "high", "medium"]),
                "verified": random.choice([True, False]),
                "timestamp": self._random_timestamp(),
                "source": random.choice(["Twitter", "Facebook", "Instagram"])
            }
            feed.append(post)
        return feed
    
    def generate_alerts(self) -> List[Dict]:
        """Generate real-time alerts"""
        alert_types = [
            {"type": "Building Collapse", "category": "infrastructure"},
            {"type": "Flash Flood Warning", "category": "environmental"},
            {"type": "Infrastructure Failure", "category": "infrastructure"},
            {"type": "Medical Emergency", "category": "rescue"},
            {"type": "Evacuation Order", "category": "rescue"},
            {"type": "Resource Shortage", "category": "logistics"},
            {"type": "Rescue Operation", "category": "rescue"},
            {"type": "Search and Rescue", "category": "rescue"}
        ]
        
        alerts = []
        for i in range(12):
            alert_type = random.choice(alert_types)
            alert = {
                "id": f"alert_{i+1}",
                "type": alert_type["type"],
                "category": alert_type["category"],
                "severity": random.choice(["critical", "high", "medium"]),
                "location": random.choice(self.locations),
                "coordinates": {
                    "lat": self.base_lat + random.uniform(-0.1, 0.1),
                    "lon": self.base_lon + random.uniform(-0.1, 0.1)
                },
                "description": f"Emergency situation detected in {random.choice(self.locations)}",
                "affected_population": random.randint(50, 2000),
                "status": random.choice(["active", "responding", "resolved"]),
                "timestamp": self._random_timestamp(),
                "priority_score": round(random.uniform(0.5, 1.0), 2)
            }
            alerts.append(alert)
        return alerts
    
    def _random_timestamp(self) -> str:
        """Generate random recent timestamp"""
        now = datetime.now()
        random_time = now - timedelta(
            hours=random.randint(0, 12),
            minutes=random.randint(0, 59)
        )
        return random_time.isoformat()
