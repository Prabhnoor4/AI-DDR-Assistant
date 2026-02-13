class DataNormalizer:
    #normalizes extracted inspection and thermal data into consistent internal structure

    @staticmethod
    def normalize(inspection_data: dict, thermal_data: dict) -> dict:
        #returns unified structure

        normalized = {
            "areas": {},
            "thermal_readings": thermal_data.get("thermal_readings", [])
        }

        for area in inspection_data.get("areas", []):
            name = area.get("area_name", "Unknown Area")

            normalized["areas"][name] = {
                "negative_findings": area.get("negative_findings", []),
                "positive_findings": area.get("positive_findings", [])
            }

        return normalized
