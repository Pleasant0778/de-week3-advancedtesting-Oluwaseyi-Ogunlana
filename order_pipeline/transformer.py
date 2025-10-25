
import json, re
from typing import List, Dict, Any
from order_pipeline.validator import Validator 



class Transformer():

  text_field = ['item','payment_status']



  def __init__(self,  rows_to_skip : List[Dict[str, Any]] = []):

    #self.required_data = required_data

    self.rows_to_skip = Validator().rows_to_skip


  def convert(self, required_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for data in  required_data:
       for field in Validator.positive_fields:
          if (field == 'quantity') & (not isinstance(data[field], (int, float, type(None)))):
              if data[field].isdigit():
                data[field] =  int(data[field])
          if (field != 'quantity') & (not isinstance(data[field], (int, float, type(None)))):
              if float(data[field]):
                data[field] =  float(data[field])
    return required_data


  def normalize(self, required_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for field in Transformer.text_field:
       for data in required_data:
          data[field] =   data[field].strip().lower()
    return required_data

  def check_optional_fields(self, skipped_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    print('inside optional')
    #self.rows_to_skip = Validator().rows_to_skip
    print(skipped_rows)
    additional_required = []
    for field in Validator.positive_fields:
        for data in skipped_rows:  
            if field == 'quantity':
                if (data[field] in ( None,"N/A","")) & (data['price'] is not None) & (data['total'] is not None):
                    data['quantity'] = data['total'] / data['price']
                    additional_required.append(data)
                    self.rows_to_skip = [row for row in skipped_rows if row not in additional_required]
            if field == 'price':
                if (data[field] in ( None,"N/A","")) & (data['quantity'] is not None) & (data['total'] is not None):
                    data['price'] = data['total'] / data['quantity']
                    additional_required.append(data)
                    self.rows_to_skip = [row for row in skipped_rows if row not in additional_required]
            if field == 'total':
                if (data[field] in ( None,"N/A","")) & (data['price'] is not None) & (data['quantity'] is not None):
                    data['total'] = data['quantity'] * data['price']
                    additional_required.append(data)
                    self.rows_to_skip = [row for row in skipped_rows if row not in additional_required]
    print(self.rows_to_skip)
    print(additional_required)
             

    return additional_required
    #done with optional fields   
    

  def recalculate_total(self, required_data: List[Dict[str, Any]] ) -> List[Dict[str, Any]]:

    for data in required_data:
       data['total'] = data['quantity'] * data['price']

    return required_data

  def transform_timestamp(self):
    pass
  
  def transform(self, required_data: List[Dict[str, Any]], skipped_rows: List[Dict[str, Any]] ) -> List[Dict[str, Any]]:
    converted_data = self.convert(required_data)
    normalized_data = self.normalize(converted_data)
    new_required_data =  self.recalculate_total(normalized_data)

    self.rows_to_skip = skipped_rows
    print('normalizing skipped record')
    #self.rows_to_skip = skipped_rows
    print(skipped_rows)
    print('...checking skipped rows')
    conv_skip_data = self.convert(skipped_rows)
    norm_skip_data = self.normalize(conv_skip_data)
    check_optional = self.check_optional_fields(norm_skip_data)
    print(norm_skip_data)
    print('checked optional')
    print(check_optional)
    print('new required data')
    print(new_required_data) 
    self.rows_to_skip = [row for row in self.rows_to_skip if row not in check_optional]
    for option_data in check_optional:
       new_required_data.append(option_data)
    print('final required data')
    print(new_required_data)

    return new_required_data
    #return new_required_data


