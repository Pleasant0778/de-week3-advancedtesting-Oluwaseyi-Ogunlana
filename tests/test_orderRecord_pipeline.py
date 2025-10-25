from order_pipeline.reader import Reader
from order_pipeline.validator import Validator
from order_pipeline.transformer import Transformer
from order_pipeline.analyzer import Analyzer
from order_pipeline.exporter import Exporter
import json, pytest


input_file_path = 'C:/Users/Personal/data_epic/week_3/shoplink.json'
correct_file_format = 'json'
invalid_file_format = 'csv'

@pytest.fixture
def init_pipeline():
    return [
Reader(input_file_path, correct_file_format),
Reader(input_file_path, invalid_file_format),
Validator(),
Transformer(),
Analyzer(),
Exporter()

    ]

@pytest.fixture
def sample_invalid_data():
    return [
{"order_id": "ORD001", "timestamp": "2025-10-19T08:00:00Z","item": "Wireless Mouse", "quantity": 2, "total": "$31.98"},
{"order_id": "ORD002", "timestamp": "2025-10-19 08:05","item": "N/A","quantity": "1","price": "12.50","total": "12.50","payment_status": "PAID"},
{"order_id": "ORD003", "timestamp": "19/10/2025 08:10 AM","item": "USB Cable", "quantity": -3, "price": "N/A", "total": "$12.50", "payment_status": "pending" } , 
{"order_id": "ORD004", "timestamp": "19/10/2025 08:10 AM","item": "USB Cable", "quantity":12.0, "price": "N120.50", "total": 15, "payment_status": None}
]


@pytest.fixture
def sample_optional_data():
    return [
{"order_id": "ORD001", "timestamp": "2025-10-19 08:05","item": "N/A","quantity": "1","price": None,"total": "12.50","payment_status": "PAID"  },
{"order_id": "ORD002", "timestamp": "19/10/2025 08:10 AM","item": "USB Cable", "quantity": None, "price": "N2.5", "total": "$12.50", "payment_status": "pending" },
{"order_id": "ORD003", "timestamp": "19/10/2025 08:10 AM","item": "USB Cable", "quantity":"12", "price": "N120.50", "total": None, "payment_status": 'PaiD' }

]


@pytest.fixture
def sample_valid_data():
    return [
{"order_id": "ORD001", "timestamp": "2025-10-19T08:00:00Z","item": "Wireless Mouse", "quantity": 2, "price": "$15.99","total": "$31.98","payment_status": "paid"},
{"order_id": "ORD002", "timestamp": "2025-10-19 08:05","item": "Laptop Sleeve","quantity": "1","price": "N12.50","total": "$12.50","payment_status": "PAID"  },
{"order_id": "ORD003", "timestamp": "19/10/2025 08:10 AM","item": "USB Cable", "quantity": -3, "price": "5usd", "total": 15, "payment_status": "pending" }
]


def test_reader_on_valid_format(init_pipeline):
    reader = init_pipeline[0]
    data = list(reader.read_data())
    assert isinstance(data, list)
    assert all(isinstance(record, dict) for record in data)


def test_reader_invalid_format(init_pipeline):
    reader = init_pipeline[1]
    with pytest.raises(ValueError):
        data = list(reader.read_data())


def test_validator_on_invalid(sample_invalid_data, init_pipeline):
    validator = init_pipeline[2]
    validator.validate_data(sample_invalid_data)
    #print(validator.required_data)
    assert len(validator.required_data) == 0
    assert len(validator.rows_to_skip) == 3


def test_validator_on_optional(sample_optional_data,init_pipeline):
    validator = init_pipeline[2]
    validator.validate_data(sample_optional_data)
    rows_to_skip  = validator.rows_to_skip
    #print(validator.required_data)
    assert len(validator.required_data) == 0
    assert len(rows_to_skip) == 3

def test_transformer_valid_compute(sample_valid_data,init_pipeline):
    validator = init_pipeline[2]
    validator.validate_data(sample_valid_data)
    transform = init_pipeline[3]
    assert len(transform.transform(validator.required_data, validator.rows_to_skip)) == 3
    


def test_transformer_optional_compute(sample_optional_data,init_pipeline):
    validator = init_pipeline[2]
    validator.validate_data(sample_optional_data)
    transform = init_pipeline[3]
    assert len(transform.transform(validator.required_data, validator.rows_to_skip)) == 3


def test_analyser_compute(sample_valid_data,init_pipeline):
    validator =  init_pipeline[2]
    validator.validate_data(sample_valid_data)
    transform = init_pipeline[3]
    analysed_data = init_pipeline[4].compute(transform.transform(validator.required_data, validator.rows_to_skip))
    assert analysed_data['total_revenue'] == round((12.50 + 31.98),2)
    assert analysed_data['average_revenue'] == round(((12.50 + 31.98) / 2),2)
    assert analysed_data['payment_status_summary'] == {'paid': 2, 'pending': 1}
"""
def test_exporter_compute(sample_valid_data, tmp_path, init_pipeline):
    validator =  init_pipeline[2]
    validator.validate_data(sample_valid_data)
    transform = init_pipeline[3]
    analysed_data = init_pipeline[4].compute(transform.transform(validator.required_data, validator.rows_to_skip))
    exporter = init_pipeline[5]
    output_file = tmp_path / "output.json"
    exporter.export_data(analysed_data, output_file)
    with open(output_file, 'r') as file:
        data = json.load(file)
    assert data == analysed_data
"""
@pytest.mark.parametrize("analyzed_data",[
        '{"total_revenue": 44.48,"average_revenue": 22.24, "payment_status_summary": {"paid": 2, "pending": 1}}'
]
)
def test_exporter_compute(sample_valid_data, tmp_path, init_pipeline,analyzed_data):
    validator =  init_pipeline[2]
    validator.validate_data(sample_valid_data)
    transform = init_pipeline[3]
    analysed = init_pipeline[4].compute(transform.transform(validator.required_data, validator.rows_to_skip))
    exporter = init_pipeline[5]
    output_file = tmp_path / "output.json"
    exporter.export_data(analysed, output_file)
    #with open(output_file, 'r') as file:
     #   data = json.load(file)
    #assert data == analysed_data
    assert json.load(open(output_file, 'r')) == json.loads(analyzed_data)




def test_integration(sample_valid_data, tmp_path, init_pipeline):
    read_data = list(init_pipeline[0].read_data())
    val_data = init_pipeline[2].validate_data(read_data)
    tran_data= init_pipeline[3].transform(init_pipeline[2].required_data, init_pipeline[2].rows_to_skip)
    analysed_data = init_pipeline[4].compute(tran_data)
    init_pipeline[5].export_data(tran_data,tmp_path/ "cleaned_order_test.json")
    init_pipeline[5].export_data(analysed_data,tmp_path/  'analyzer_summary_test.json')
   
   
    assert len(tran_data) == 8
    assert json.load(open(tmp_path/  'analyzer_summary_test.json', 'r')) == analysed_data
    

