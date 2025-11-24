import json
import os
import time
from typing import Dict, Any

ANALYTICS_FILE = os.path.join(os.path.dirname(__file__), "analytics", "records.jsonl")

class AnalyticsLogger:
    def log_query(self, data: Dict[str, Any]):
        record = {
            "timestamp": time.time(),
            **data
        }
        with open(ANALYTICS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def get_records(self) -> list:
        if not os.path.exists(ANALYTICS_FILE):
            return []
        
        records = []
        with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return records[::-1]  # Return newest first
