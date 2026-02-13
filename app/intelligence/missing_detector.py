class MissingDetector:
    #detects missing or unclear required information for final DDR generation
    
    @staticmethod
    def detect(normalized_data: dict) -> list:
        #returns list of missing information statements
        missing = []
        
        areas = normalized_data.get("areas", {})
        
        if not areas:
            missing.append("No impacted areas identified.")
        
        # Check if any area has no findings
        for area_name, content in areas.items():
            negative = content.get("negative_findings", [])
            positive = content.get("positive_findings", [])
            
            # Handle both string and list types
            if isinstance(negative, str):
                negative = [negative] if negative else []
            if isinstance(positive, str):
                positive = [positive] if positive else []
            
            if not negative and not positive:
                missing.append(f"No findings available for {area_name}.")
        
        # Check if no thermal readings present
        if not normalized_data.get("thermal_readings"):
            missing.append("Thermal readings: Not Available.")
        
        return missing
