class ConflictDetector:
    # Detects conflicting information in the normalized data
    
    @staticmethod
    def detect(normalized_data: dict) -> list:
        # Returns list of conflict descriptions
        conflicts = []
        
        for area_name, content in normalized_data.get("areas", {}).items():
            # Ensure findings are lists, not strings
            negative_findings = content.get("negative_findings", [])
            positive_findings = content.get("positive_findings", [])
            
            # Convert to list if string (defensive programming)
            if isinstance(negative_findings, str):
                negative_findings = [negative_findings] if negative_findings else []
            if isinstance(positive_findings, str):
                positive_findings = [positive_findings] if positive_findings else []
            
            # Check for "no leakage" but also mentions "dampness"
            no_leakage = any("no leakage" in f.lower() for f in negative_findings)
            dampness = any("damp" in f.lower() or "seepage" in f.lower()
                           for f in negative_findings)
            
            if no_leakage and dampness:
                conflicts.append(
                    f"Conflict in {area_name}: 'No leakage' and dampness/seepage both reported."
                )
            
            # Check for plumbing marked both yes and no
            all_findings = negative_findings + positive_findings
            plumbing_yes = any("plumbing" in f.lower() and "yes" in f.lower()
                               for f in all_findings)
            plumbing_no = any("plumbing" in f.lower() and "no" in f.lower()
                              for f in all_findings)
            
            if plumbing_yes and plumbing_no:
                conflicts.append(
                    f"Conflict in {area_name}: Plumbing reported both Yes and No."
                )
        
        return conflicts
