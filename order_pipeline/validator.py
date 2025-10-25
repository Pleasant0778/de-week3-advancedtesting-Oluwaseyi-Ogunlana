
import json, re
from typing import List, Dict, Any
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
   level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s"

)

class Validator():

  required_fields = ['order_id', 'timestamp', 'item', 'quantity', 'price', 'payment_status', 'total']
  positive_fields = ['quantity','price','total']


  def __init__(self):
    self.data_list = []
    self.required_data = []
    self.rows_to_skip = []


  def check_records_with_valid_cols(self):
    for data in self.data_list:
      if len(data.keys()) == len(Validator.required_fields):
        no_valid_col = [True for field in Validator.required_fields  if field in data]
        if all(no_valid_col):
           self.required_data.append(data)
      else:
         logger.info('The length of the row is %s, it not up to what is required %s', len(data.keys()), len(Validator.required_fields))

    logger.info('Checked for valid records!!!')

  def skip_invalid_record(self):

    
    for field in Validator.required_fields:
        for data in self.required_data:
            if (data[field] == "N/A") |  (data[field] == "") | (data[field] is None):
                self.rows_to_skip.append(data)
    print(self.rows_to_skip)
    self.rows_to_skip = list({tuple(d.items()): d for d in self.rows_to_skip}.values())

    self.required_data = [data for data in self.required_data if data not in self.rows_to_skip]
    print(self.required_data)

  def extract_numeric(self):
    print('inside convert')
    print(self.required_data)
                  

    for data in self.required_data:
       for field in Validator.positive_fields:
          if (field == 'quantity') & (not isinstance(data[field], (int, float,type(None)))):
            found = re.findall(r'[\d?\.?\d+]+',data[field])
            if not found:
               continue
            try:
               data[field] =   found[0]
            except ValueError:
               continue
               raise ValueError('Quantity is invalid')
          if (field != 'quantity') & (not isinstance(data[field], (int, float,type(None)))):
            found = re.findall(r'[\d+\.?\d+]+',data[field])
            if not found:
               continue
            try:
               data[field] =  found[0]
            except ValueError:
               continue
               raise ValueError(f'{field} is invalid')
            
          

       for field in Validator.positive_fields:
        if isinstance(data[field], (int, float)):
          #print(data[field])
          data[field] = abs(data[field])
    
  
  def check_optional_fields(self):
    print('inside optional')
    print(self.rows_to_skip)
    for field in Validator.positive_fields:
        for data in self.rows_to_skip:  
            if field == 'quantity':
                if (data[field] in ( None,"N/A","")) & (data['price'] is not None) & (data['total'] is not None):
                    data['quantity'] = data['total'] / data['price']
                    self.required_data.append(data)
                    self.rows_to_skip = [row for row in self.rows_to_skip if row not in self.required_data]
            if field == 'price':
                if (data[field] in ( None,"N/A","")) & (data['quantity'] is not None) & (data['total'] is not None):
                    data['price'] = data['total'] / data['quantity']
                    self.required_data.append(data)
                    self.rows_to_skip = [row for row in self.rows_to_skip if row not in self.required_data]
            if field == 'total':
                if (data[field] in ( None,"N/A","")) & (data['price'] is not None) & (data['quantity'] is not None):
                    data['total'] = data['quantity'] * data['price']
                    self.required_data.append(data)
                    self.rows_to_skip = [row for row in self.rows_to_skip if row not in self.required_data]
            
    #done with optional fields   
    print(self.rows_to_skip)
    print(self.required_data)
    

  def validate_data(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    self.data_list = data_list
    self.check_records_with_valid_cols()
    #self.skip_invalid_record()
    self.extract_numeric()
    self.skip_invalid_record()
    #self.check_optional_fields()

    valid_data = self.required_data

    return valid_data



