
import json, re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s"

)

class Analyzer:
  def __init__(self):
    self.required_data = []



  def total_revenue(self) -> float:
    logging.debug('...computing total revenue')
    return round(sum([ data['total'] for data in self.required_data if data['payment_status'] == 'paid']),2)
    
  def average_revenue(self) -> float:
    logging.debug('...computing average revenue')
    total_revenue_list = [data['total'] for data in self.required_data if data['payment_status'] == 'paid']

    return round(sum(total_revenue_list) / len(total_revenue_list),2)
    
  
  def payment_status_summary(self) -> Dict[str, float]:
    logging.debug('...generating oayment summary')
    payment_summary = {}

    total_revenue_list = [data['payment_status'] for data in self.required_data]

    for status in total_revenue_list:
      payment_summary[status] = payment_summary.get(status, 0) + 1
      
    return payment_summary
   
  def compute(self, require_data: List[Dict[str, Any]]) :#-> Dict[str, Any]:
    self.required_data = require_data
    logging.info('Analysing loaded data')

    #print(self.required_data)
    summary = {
        "total_revenue": self.total_revenue(),
        "average_revenue": self.average_revenue(),
        "payment_status_summary": self.payment_status_summary()
    }

    #with open('analyzer_summary11.json', 'w') as file:
    #  json.dump(summary, file)#, indent=4)

    return {
        "total_revenue": self.total_revenue(),
        "average_revenue": self.average_revenue(),
        "payment_status_summary": self.payment_status_summary()
    }