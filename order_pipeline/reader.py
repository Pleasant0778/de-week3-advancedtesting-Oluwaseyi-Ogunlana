import json, re
from typing import List, Dict, Any, Iterable
from dataclasses  import dataclass, asdict
import logging
 


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(message)s")



@dataclass
class OrderRecord:
    order_id: str
    timestamp: str
    item: str
    quantity: int
    price: float
    payment_status: str
    total: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Reader():

  def __init__(self, file_path:str, file_format:str = None):

    self.file_path  = file_path
    self.file_format = file_format



  def read_data(self) -> Iterable[Dict[str, str]]:
    logger.info("Welcome to Order Pipeline!!!")
    logger.info("Reader class called to read %s with %s format", self.file_path, self.file_format)
    if self.file_format != 'json':
        logger.info("The file format %s provided is not supported by the reader", self.file_format)
        raise ValueError('The file format provided is not supported by the reader')
    else:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                if len(data) == 0:
                    logger.debug("The file in the filepath - %s provided is empty", self.file_path)
                    raise ValueError('The file provided is empty!!!')
                for record in data:
                    yield record  
        except FileNotFoundError:
            logger.debug("The file cannot be found in %s", self.file_path)
            #print('Please check the file path you provided!!!')





   
            


"""

if __name__ == "__main__":
    read = Reader('C:/Users/Personal/data_epic/week_3/shoplink.json', file_format='json')
    #read = Reader('/content/shoplink.json', file_format='json')

    kk = read.read_data()

    val = Validator(kk)



    #print(val.data_list)


    print(kk)
    print(len(kk))

    val.validate()

    print(val.required_data)


    print(val.skip_invalid_record())


    print(val.required_data)



    print(val.convert_data_type())


    print(val.required_data)
    #print(val.required_data_after_skip)


    trans = Transformer(val.required_data, val.rows_to_skip)

    trans.convert()

    print(trans.required_data)

    print(trans.normalize())

    trans.check_skip_list()
    print(trans.required_data)
    
    
    anal = Analyzer(trans.required_data)

    print(anal.total_revenue())
    print(anal.average_revenue())
    
    print(anal.payment_status_aummary())

    exp = Exporter()
    exp.export_data(trans.required_data,'shoplink_cleaned.json')
    #print(val.required_data)


"""