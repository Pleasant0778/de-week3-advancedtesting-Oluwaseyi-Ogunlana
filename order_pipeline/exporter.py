import json, re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s")

class Exporter:
  
  def export_data(self, data: List[Dict[str, Any]], file_path: str, file_format: str = 'json'):
    logging.info('Exporting data as %s ', file_path)
    if data is not None:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)