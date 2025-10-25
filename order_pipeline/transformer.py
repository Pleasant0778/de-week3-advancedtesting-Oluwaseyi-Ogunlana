
import json, re
from typing import List, Dict, Any
from order_pipeline.validator import Validator 
import logging
from dateutil import parser

logger = logging.getLogger(__name__)
logging.basicConfig(
   level=logging.INFO,
   format="%(acstime)s - %(levelname)s : %(message)s"

)


class Transformer:

  text_field = ['item','payment_status']



  def __init__(self,  rows_to_skip : List[Dict[str, Any]] = []):

    #self.required_data = required_data

    self.rows_to_skip = Validator().rows_to_skip


  def convert(self, required_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logging.info('Converting string literals that are digit to numeric')
    for data in  required_data:
       for field in Validator.positive_fields:
          if (field == 'quantity') & (not isinstance(data[field], (int, float, type(None)))):
              if data[field].isdigit():
                data[field] =  int(data[field])
                logging.debug('Converted %s to numeric', field)
          if (field != 'quantity') & (not isinstance(data[field], (int, float, type(None)))):
              if float(data[field]):
                data[field] =  float(data[field])
                logging.debug('Converted %s to numeric', field)
    logging.info('Done converting records to numeric')
    return required_data


  def normalize(self, required_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logging.info('Normalizing string data to lower case')
    for field in Transformer.text_field:
       for data in required_data:
          data[field] =   data[field].strip().lower()
    logging.info("Done normalizing string data")
    return required_data

  def check_optional_fields(self, skipped_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logging.info('Checking optional field to compute the value')
    #self.rows_to_skip = Validator().rows_to_skip
    logging.info('The size of skipped ros is %s: ', len(skipped_rows))
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
    #print(self.rows_to_skip)
    #print(additional_required)

    logging.info('The size of skipped rows after checking for optional field is %s: ', len(self.rows_to_skip))
    logging.info('The size of additional rows from skipped rows %s: ', len(additional_required))

             

    return additional_required
    #done with optional fields   
    

  def recalculate_total(self, required_data: List[Dict[str, Any]] ) -> List[Dict[str, Any]]:
    logging.info('Recalculating total!!!')
    for data in required_data:
       data['total'] = data['quantity'] * data['price']

      
    logging.info('Done recalculating totals!!!')

    return required_data

  def transform_timestamp(self, required_data):
      #
      for data in required_data:
          timestamp = data.get("timestamp", None)
          try:
              if timestamp and timestamp not in ( None,"N/A",""):
                  parsed_timestamp = parser.parse(timestamp)
                  data["timestamp"] = parsed_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")  
              
          except (ValueError, TypeError):
              data["timestamp"] = timestamp
      return required_data
  
  def check_duplicates(self, required_data: List[Dict[str, Any]] ):
     logging.info('Checking and removing duplicates')
     final_required_data = []
     not_duplicated = set()

      
     for data in required_data:
        frozen = frozenset(data.items())
        if frozen not in not_duplicated:
           final_required_data.append(data)
           not_duplicated.add(frozen)
            
           
     
     #final_required_data = [ dict(unique) for unique in {frozenset(data.items()) for data in required_data} ]
     
     logging.info('Done removing duplicate')
     logging.info('Size before removing duplicate %s ', len(required_data))
     logging.info('Size after removing duplicate %s ', len(final_required_data))
     return sorted(final_required_data, key= lambda data:data['order_id'])

  
  def transform(self, required_data: List[Dict[str, Any]], skipped_rows: List[Dict[str, Any]] ) -> List[Dict[str, Any]]:
    converted_data = self.convert(required_data)
    normalized_data = self.normalize(converted_data)
    formart_timestamp = self.transform_timestamp(normalized_data)
    new_required_data =  self.recalculate_total(normalized_data)

    self.rows_to_skip = skipped_rows
    logging.info('normalizing skipped record')
    #print('normalizing skipped record')
    #self.rows_to_skip = skipped_rows
    #print(skipped_rows)
    logging.info('...checking skipped rows')
    #print('...checking skipped rows')
    conv_skip_data = self.convert(skipped_rows)
    norm_skip_data = self.normalize(conv_skip_data)
    check_optional = self.check_optional_fields(norm_skip_data)
    #print(norm_skip_data)
    #print('checked optional')
    #print(check_optional)
    #print('new required data')
    #print(new_required_data) 
    self.rows_to_skip = [row for row in self.rows_to_skip if row not in check_optional]
    for option_data in check_optional:
       new_required_data.append(option_data)

    final_required_data = self.check_duplicates(new_required_data)
    
    logging.info('The final required data with size %s is ready!!!', len(final_required_data))
    #print('final required data')
    #print(new_required_data)

    return final_required_data
    #return new_required_data


