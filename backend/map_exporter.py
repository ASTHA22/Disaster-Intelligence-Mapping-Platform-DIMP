"""
Map Export Service
Generate PDF and image exports of disaster maps
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from typing import Dict, List
import io
import json

class MapExporter:
    """Export disaster maps to PDF and images"""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        
    def generate_pdf_report(self, disaster_data: Dict, statistics: Dict) -> bytes:
        """
        Generate comprehensive PDF report
        
        Args:
            disaster_data: Dict with zones, floods, infrastructure, etc.
            statistics: Dict with summary statistics
            
        Returns:
            PDF bytes
        """
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Title Page
        self._draw_title_page(c, statistics)
        c.showPage()
        
        # Summary Page
        self._draw_summary_page(c, statistics, disaster_data)
        c.showPage()
        
        # Disaster Zones Detail
        if disaster_data.get('zones'):
            self._draw_zones_page(c, disaster_data['zones'])
            c.showPage()
        
        # Flood Areas Detail
        if disaster_data.get('flood_areas'):
            self._draw_floods_page(c, disaster_data['flood_areas'])
            c.showPage()
        
        # Infrastructure Damage
        if disaster_data.get('infrastructure'):
            self._draw_infrastructure_page(c, disaster_data['infrastructure'])
            c.showPage()
        
        # Alerts Page
        if disaster_data.get('alerts'):
            self._draw_alerts_page(c, disaster_data['alerts'])
            c.showPage()
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_title_page(self, c: canvas.Canvas, statistics: Dict):
        """Draw title page"""
        # Header
        c.setFillColor(colors.HexColor('#ef4444'))
        c.rect(0, self.page_height - 2*inch, self.page_width, 2*inch, fill=True)
        
        # Title
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(self.page_width/2, self.page_height - 1.2*inch, 
                           "DIMP")
        
        c.setFont("Helvetica", 16)
        c.drawCentredString(self.page_width/2, self.page_height - 1.6*inch, 
                           "Disaster Intelligence Mapping Platform")
        
        # Report Info
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(self.page_width/2, self.page_height - 3*inch, 
                           "Disaster Assessment Report")
        
        c.setFont("Helvetica", 12)
        c.drawCentredString(self.page_width/2, self.page_height - 3.5*inch, 
                           f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}")
        
        # Key Statistics Box
        y_pos = self.page_height - 5*inch
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.rect(inch, y_pos - 2*inch, self.page_width - 2*inch, 2*inch, fill=True)
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(self.page_width/2, y_pos - 0.5*inch, "Summary Statistics")
        
        c.setFont("Helvetica", 11)
        stats_y = y_pos - 1*inch
        stats = [
            f"Damaged Buildings: {statistics.get('damaged_buildings', 0):,}",
            f"Flooded Zones: {statistics.get('flooded_zones', 0)}",
            f"Displaced Population: {statistics.get('displaced_population', 0):,}",
            f"Active Rescue Operations: {statistics.get('rescue_operations_active', 0)}"
        ]
        
        for stat in stats:
            c.drawCentredString(self.page_width/2, stats_y, stat)
            stats_y -= 0.3*inch
        
        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        c.drawCentredString(self.page_width/2, 0.5*inch, 
                           "Confidential - For Emergency Response Use Only")
    
    def _draw_summary_page(self, c: canvas.Canvas, statistics: Dict, disaster_data: Dict):
        """Draw summary page with overview"""
        # Header
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor('#1e293b'))
        c.drawString(inch, self.page_height - inch, "Executive Summary")
        
        # Divider
        c.setStrokeColor(colors.HexColor('#ef4444'))
        c.setLineWidth(2)
        c.line(inch, self.page_height - 1.2*inch, self.page_width - inch, self.page_height - 1.2*inch)
        
        y_pos = self.page_height - 1.8*inch
        
        # Overview Section
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(inch, y_pos, "Situation Overview")
        y_pos -= 0.4*inch
        
        c.setFont("Helvetica", 11)
        overview_text = [
            f"Total Affected Area: {statistics.get('total_affected_area_km2', 0)} km²",
            f"Emergency Shelters Operational: {statistics.get('emergency_shelters', 0)}",
            f"Rescue Operations Active: {statistics.get('rescue_operations_active', 0)}",
            f"Last Updated: {statistics.get('last_updated', 'N/A')}"
        ]
        
        for text in overview_text:
            c.drawString(inch + 0.2*inch, y_pos, f"• {text}")
            y_pos -= 0.3*inch
        
        y_pos -= 0.3*inch
        
        # Severity Breakdown
        c.setFont("Helvetica-Bold", 14)
        c.drawString(inch, y_pos, "Severity Breakdown")
        y_pos -= 0.4*inch
        
        zones = disaster_data.get('zones', [])
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for zone in zones:
            severity = zone.get('severity', 'low')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        c.setFont("Helvetica", 11)
        for severity, count in severity_counts.items():
            color_map = {
                'critical': '#dc2626',
                'high': '#ea580c',
                'medium': '#f59e0b',
                'low': '#84cc16'
            }
            c.setFillColor(colors.HexColor(color_map[severity]))
            c.rect(inch + 0.2*inch, y_pos - 0.1*inch, 0.15*inch, 0.15*inch, fill=True)
            c.setFillColor(colors.black)
            c.drawString(inch + 0.5*inch, y_pos, f"{severity.capitalize()}: {count} zones")
            y_pos -= 0.3*inch
        
        y_pos -= 0.3*inch
        
        # Priority Actions
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor('#dc2626'))
        c.drawString(inch, y_pos, "Priority Actions Required")
        y_pos -= 0.4*inch
        
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        actions = [
            "Deploy rescue teams to critical zones",
            "Establish evacuation routes from flooded areas",
            "Set up emergency medical stations",
            "Coordinate shelter assignments for displaced population",
            "Monitor infrastructure stability in damaged zones"
        ]
        
        for action in actions:
            c.drawString(inch + 0.2*inch, y_pos, f"• {action}")
            y_pos -= 0.3*inch
        
        # Page number
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawRightString(self.page_width - inch, 0.5*inch, "Page 2")
    
    def _draw_zones_page(self, c: canvas.Canvas, zones: List[Dict]):
        """Draw disaster zones detail page"""
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor('#1e293b'))
        c.drawString(inch, self.page_height - inch, "Disaster Zones")
        
        c.setStrokeColor(colors.HexColor('#ef4444'))
        c.setLineWidth(2)
        c.line(inch, self.page_height - 1.2*inch, self.page_width - inch, self.page_height - 1.2*inch)
        
        y_pos = self.page_height - 1.8*inch
        
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        for i, zone in enumerate(zones[:10]):  # Limit to 10 zones per page
            if y_pos < 2*inch:
                break
            
            # Zone header
            c.setFont("Helvetica-Bold", 12)
            c.drawString(inch, y_pos, f"{zone.get('name', 'Unknown')}")
            y_pos -= 0.3*inch
            
            c.setFont("Helvetica", 10)
            details = [
                f"Severity: {zone.get('severity', 'N/A').capitalize()}",
                f"Damage Score: {zone.get('damage_score', 0):.2f}",
                f"Affected Area: {zone.get('affected_area_km2', 0)} km²",
                f"Coordinates: {zone.get('coordinates', {}).get('lat', 0):.4f}, {zone.get('coordinates', {}).get('lon', 0):.4f}"
            ]
            
            for detail in details:
                c.drawString(inch + 0.2*inch, y_pos, f"• {detail}")
                y_pos -= 0.25*inch
            
            y_pos -= 0.3*inch
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawRightString(self.page_width - inch, 0.5*inch, "Page 3")
    
    def _draw_floods_page(self, c: canvas.Canvas, floods: List[Dict]):
        """Draw flood areas detail page"""
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor('#1e293b'))
        c.drawString(inch, self.page_height - inch, "Flood-Affected Areas")
        
        c.setStrokeColor(colors.HexColor('#3b82f6'))
        c.setLineWidth(2)
        c.line(inch, self.page_height - 1.2*inch, self.page_width - inch, self.page_height - 1.2*inch)
        
        y_pos = self.page_height - 1.8*inch
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        for flood in floods[:12]:
            if y_pos < 2*inch:
                break
            
            c.setFont("Helvetica-Bold", 11)
            c.drawString(inch, y_pos, f"{flood.get('area_name', 'Unknown Area')}")
            y_pos -= 0.3*inch
            
            c.setFont("Helvetica", 10)
            c.drawString(inch + 0.2*inch, y_pos, 
                        f"• Water Level: {flood.get('water_level_meters', 0):.1f}m | "
                        f"Affected: {flood.get('affected_area_km2', 0)} km²")
            y_pos -= 0.4*inch
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawRightString(self.page_width - inch, 0.5*inch, "Page 4")
    
    def _draw_infrastructure_page(self, c: canvas.Canvas, infrastructure: List[Dict]):
        """Draw infrastructure damage page"""
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor('#1e293b'))
        c.drawString(inch, self.page_height - inch, "Infrastructure Damage")
        
        c.setStrokeColor(colors.HexColor('#f59e0b'))
        c.setLineWidth(2)
        c.line(inch, self.page_height - 1.2*inch, self.page_width - inch, self.page_height - 1.2*inch)
        
        y_pos = self.page_height - 1.8*inch
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        for infra in infrastructure[:15]:
            if y_pos < 2*inch:
                break
            
            c.drawString(inch, y_pos, 
                        f"• {infra.get('type', 'Unknown').capitalize()}: "
                        f"{infra.get('name', 'N/A')} - "
                        f"{infra.get('status', 'Unknown')}")
            y_pos -= 0.3*inch
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawRightString(self.page_width - inch, 0.5*inch, "Page 5")
    
    def _draw_alerts_page(self, c: canvas.Canvas, alerts: List[Dict]):
        """Draw active alerts page"""
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor('#1e293b'))
        c.drawString(inch, self.page_height - inch, "Active Alerts")
        
        c.setStrokeColor(colors.HexColor('#dc2626'))
        c.setLineWidth(2)
        c.line(inch, self.page_height - 1.2*inch, self.page_width - inch, self.page_height - 1.2*inch)
        
        y_pos = self.page_height - 1.8*inch
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        for alert in alerts[:10]:
            if y_pos < 2*inch:
                break
            
            c.setFont("Helvetica-Bold", 11)
            c.drawString(inch, y_pos, f"{alert.get('type', 'Alert').upper()}")
            y_pos -= 0.3*inch
            
            c.setFont("Helvetica", 10)
            c.drawString(inch + 0.2*inch, y_pos, 
                        f"• {alert.get('description', 'No description')}")
            y_pos -= 0.25*inch
            c.drawString(inch + 0.2*inch, y_pos, 
                        f"• Status: {alert.get('status', 'Unknown')} | "
                        f"Severity: {alert.get('severity', 'Unknown')}")
            y_pos -= 0.4*inch
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawRightString(self.page_width - inch, 0.5*inch, "Page 6")
    
    def generate_json_export(self, disaster_data: Dict) -> bytes:
        """Generate JSON export of all data"""
        json_str = json.dumps(disaster_data, indent=2, default=str)
        return json_str.encode('utf-8')
    
    def generate_csv_export(self, zones: List[Dict]) -> bytes:
        """Generate CSV export of disaster zones"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['ID', 'Name', 'Severity', 'Damage Score', 'Area (km²)', 'Latitude', 'Longitude', 'Last Updated'])
        
        # Data
        for zone in zones:
            writer.writerow([
                zone.get('id', ''),
                zone.get('name', ''),
                zone.get('severity', ''),
                zone.get('damage_score', 0),
                zone.get('affected_area_km2', 0),
                zone.get('coordinates', {}).get('lat', 0),
                zone.get('coordinates', {}).get('lon', 0),
                zone.get('last_updated', '')
            ])
        
        return output.getvalue().encode('utf-8')
