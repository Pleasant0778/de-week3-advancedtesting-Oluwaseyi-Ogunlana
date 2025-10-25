
from order_pipeline.reader import Reader
from order_pipeline.validator import Validator
from order_pipeline.transformer import Transformer
from order_pipeline.analyzer import Analyzer
from order_pipeline.exporter import Exporter
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s : %(message)s" )


class OrderPipeline:
    def __init__(self,  input_file_path: str, input_file_format: str = 'json',output_file_path: str = None):
        
        self.reader = Reader(input_file_path, input_file_format)
        
        self.validator = Validator()
        
        self.transformer = Transformer()
        
        self.analyzer = Analyzer()
        
        self.exporter = Exporter()
        
    def run_pipeline(self):
        logging.info('Reading data...')
        read_data = list(self.reader.read_data())
        logging.info('Validating data...')
        val_data = self.validator.validate_data(read_data)
        logging.info('Transforming data...')
        tran_data= self.transformer.transform(val_data, self.validator.rows_to_skip)
        logging.info('Analyzing data...')
        analysed_data = self.analyzer.compute(tran_data)
        logging.info('Exporting result...')
        self.exporter.export_data(tran_data,output_file_path)

        self.exporter.export_data(analysed_data,'analyzer_summary.json')
        logging.info('End of Order pipeline!!!')
        #print(self.validator.rows_to_skip)
        #print('#####')
        #print(self.transformer.rows_to_skip)
        



if __name__ == "__main__":
    input_file_path = 'C:/Users/Personal/data_epic/week_3/shoplink.json'
    #input_file_path = 'C:/Users/Personal/data_epic/week_3/test_json.json'
    output_file_path = 'shoplink_cleaned.json'
    #output_file_path = 'test_json_cleaned.json'
    file_format = 'json'

    orderpipeline = OrderPipeline(input_file_path, file_format, output_file_path)
    orderpipeline.run_pipeline()

    """
    read = Reader('C:/Users/Personal/data_epic/week_3/shoplink.json', file_format='json')
    #read = Reader('/content/shoplink.json', file_format='json')

    kk = read.read_data()

    kk1 = list(read.read_data())

    
    val = Validator()
    val_data = val.validate_data(kk1)

    print(kk)
    print(kk1)
    print(val_data)

    tran = Transformer()
    
    tran_data= tran.transform(val_data)

    anal = Analyzer()

    print(anal.compute(tran_data))
    """

    #print(anal.average_revenue())
    
    #print(anal.payment_status_aummary())

    #print(val.data_list)


    #print(kk)
    
    #print(kk1)

    #print(len(kk))

    #val.validate()

    #print(val.required_data)


    #print(val.skip_invalid_record())


    #print(val.required_data)



    #print(val.convert_data_type())


    #print(val.required_data)
    #print(val.required_data_after_skip)

 
    #trans = Transformer(val.required_data, val.rows_to_skip)

    #trans.convert()

    #print(trans.required_data)

    #print(trans.normalize())

    #trans.check_skip_list()
    #print(trans.required_data)
    
    
    #anal = Analyzer(trans.required_data)

    #print(anal.total_revenue())
    #print(anal.average_revenue())
    
    #print(anal.payment_status_aummary())

    #exp = Exporter()
    #exp.export_data(trans.required_data,'shoplink_cleaned.json')
    #print(val.required_data)

 
