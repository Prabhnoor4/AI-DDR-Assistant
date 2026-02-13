class AreaLinker:
    #links thermal findings to specific areas only if the area name is explicitly mentioned.

    @staticmethod
    def link(normalized_data: dict) -> dict:
        #adding thermal readings to matching areas if area name appears in thermal image_id or description.
        #otherwise, keeps them under 'General Thermal Findings'.

        thermal_readings = normalized_data.get("thermal_readings", [])
        areas = normalized_data.get("areas", {})

        #create general bucket
        normalized_data["general_thermal_findings"] = []

        for reading in thermal_readings:
            linked = False

            image_id = str(reading.get("image_id", "")).lower()

            for area_name in areas.keys():
                if area_name.lower() in image_id:
                    areas[area_name].setdefault("thermal_readings", []).append(reading)
                    linked = True
                    break

            if not linked:
                normalized_data["general_thermal_findings"].append(reading)

        return normalized_data
