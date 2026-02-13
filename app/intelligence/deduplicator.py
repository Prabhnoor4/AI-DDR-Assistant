class Deduplicator:
    #removes duplicate findings within each area

    @staticmethod
    def deduplicate(normalized_data: dict) -> dict:
        #removes duplicate negative and positive findings

        for area_name, content in normalized_data.get("areas", {}).items():

            negative = content.get("negative_findings", [])
            positive = content.get("positive_findings", [])

            # Remove exact duplicates
            content["negative_findings"] = list(set(negative))
            content["positive_findings"] = list(set(positive))

        return normalized_data
