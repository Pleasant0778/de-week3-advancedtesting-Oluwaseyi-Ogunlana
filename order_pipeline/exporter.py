import json, re
from typing import List, Dict, Any

class Exporter():
  def __init__(self):
     pass
  def export_data(self, data: List[Dict[str, Any]], file_path: str, file_format: str = 'json'):
    if data is not None:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)