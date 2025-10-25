# Order Pipeline Project

## Description
`order_pipeline` project is an ETL pipeline built with Python OOP concept for **reading**, **validating**, **transforming**, **analyzing** and **exporting** order data  and statistical summary

It reads raw order files  in JSON format, validates required fields, transforms data types e.g numeric conversion, string normalization and formating timestamps, generate analytics (like total and average revenue), and provides clean data and the result of the analysis

---

## Features
-  **Reader** – Loads order data from JSON files by providing the path to the file.  
-  **Validator** – Ensures required fields exist, checks data types, and skips invalid rows.  
-  **Transformer** – Normalizes text, converts numeric values, recalculates totals,  standardizes timestamps and generate values for optional fields that is missing in the data entry.
-  **Analyzer** – Computes metrics such as total revenue, average revenue, and payment status summary.  
-  **Exporter** – Export the processed data and the summary result as JSON file.  


---

##  Architecture Overview

```
JSON File → Reader → Validator → Transformer → Analyzer → Export (Cleaned data and Summary)
```

### Modules
| Module | Description |
|--------|--------------|
| `reader.py` | Reads order data from supported file formats (JSON). |
| `validator.py` | Validates required fields and checks for invalid or missing entries. |
| `transformer.py` | Cleans text fields, converts numeric values, handles timestamps, and recalculates totals. |
| `analyzer.py` | Aggregates metrics such as total revenue and average revenue per payment status. |
| `exporter.py` | Export the cleaned json data and also generate the output of analyser as JSON file |
| `pipeline.py` | Orchestrates the entire process (end-to-end execution). |
| `test folder` | Unit and integration testing was done to check for possible errros in the code. |

---

## Example Usage

### 1. Run the Pipeline
```bash
python -m order_pipeline.pipeline
```

### 2. Example Data (shoplink.json)
```json
[
    {
        "order_id": "ORD001",
        "timestamp": "2025-10-19T08:00:00Z",
        "item": "Wireless Mouse",
        "quantity": 2,
        "price": "$15.99",
        "total": "$31.98",
        "payment_status": "paid"
    },
    {
        "order_id": "ORD002",
        "timestamp": "2025-10-19 08:05",
        "item": "Laptop Sleeve",
        "quantity": "1",
        "price": "12.50",
        "total": "12.50",
        "payment_status": "PAID"
    },
    {
        "order_id": "ORD003",
        "timestamp": "19/10/2025 08:10 AM",
        "item": "USB Cable",
        "quantity": -3,
        "price": "5usd",
        "total": 15,
        "payment_status": "pending"
    },
    {
        "order_id": "ORD004",
        "timestamp": "2025-10-19T08:15:00Z",
        "item": "Wireless Mouse",
        "quantity": "2pcs",
        "price": "$16",
        "total": "$32.00",
        "payment_status": "paid"
    },
    {
        "order_id": "ORD005",
        "timestamp": "2025-10-19T08:20:00Z",
        "item": "",
        "quantity": 1,
        "price": "45 dollars",
        "total": 45,
        "payment_status": "refunded"
    },
    {
        "order_id": "ORD006",
        "timestamp": "2025/10/19T08:25Z",
        "item": "Phone Case",
        "quantity": 3,
        "price": "N2000",
        "total": "N6000",
        "payment_status": "PAID"
    },
    {
        "order_id": "ORD007",
        "timestamp": "2025-10-19T08:30:00Z",
        "item": "Power Bank",
        "quantity": "N/A",
        "price": "$25",
        "total": "$50",
        "payment_status": "Paid"
    },
    {
        "order_id": "ORD008",
        "timestamp": "2025-10-19T08:35:00Z",
        "item": "Charger",
        "quantity": 2,
        "price": "N4500",
        "total": "N9000",
        "payment_status": "pending"
    },
    {
        "order_id": "ORD009",
        "timestamp": "2025-10-19T08:40:00Z",
        "item": "Webcam",
        "quantity": 1,
        "price": "$29.99",
        "payment_status": "PAID"
    },

    {
        "order_id": "ORD010",
        "timestamp": "2025-10-19T08:45:00Z",
        "item": "Mouse Pad",
        "quantity": 5,
        "price": 3,
        "total": 15,
        "payment_status": "refunded"
    },
    
  {
    "order_id": "ORD003",
     "timestamp": "2025-10-19T08:10:00Z",
     "item": "Usb Cable",
     "quantity": 3,
     "price": 5.0,
     "total": 15.0,
     "payment_status": "pending"
  },
  
  {
    "order_id": "ORD011", 
    "timestamp": "19/10/2025 08:10 AM",
    "item": "USB Cable", 
    "quantity": 8.2, 
    "price":null, 
    "total": "$20.50", 
    "payment_status": "pending" 
  }

]

```

### 3. Example Output (console/log)
```
2025-10-25 11:46:57,058 - INFO:Welcome to Order Pipeline!!!
2025-10-25 11:46:57,058 - INFO:Reader class called to read C:/Users/Personal/data_epic/week_3/shoplink.json with json format
2025-10-25 11:46:57,059 - INFO:Total file read is 12
2025-10-25 11:46:57,059 - INFO:The length of the row is 6, it not up to what is required 7
2025-10-25 11:46:57,060 - INFO:Checked for valid records!!!
2025-10-25 11:46:57,060 - INFO:About to extract numberic data!!!
2025-10-25 11:46:57,060 - INFO:The number of Invalid and Optional skipped records is: 3
2025-10-25 11:46:57,060 - INFO:The number of valid records left is: 8
2025-10-25 11:46:57,060 - INFO:Done with validating data!!!
2025-10-25 11:46:57,061 - INFO:Converting string literals that are digit to numeric
2025-10-25 11:46:57,061 - INFO:Done converting records to numeric
2025-10-25 11:46:57,061 - INFO:Normalizing string data to lower case
2025-10-25 11:46:57,061 - INFO:Done normalizing string data
2025-10-25 11:46:57,062 - INFO:Recalculating total!!!
2025-10-25 11:46:57,062 - INFO:Done recalculating totals!!!
2025-10-25 11:46:57,062 - INFO:normalizing skipped record
2025-10-25 11:46:57,062 - INFO:...checking skipped rows
2025-10-25 11:46:57,062 - INFO:Converting string literals that are digit to numeric
2025-10-25 11:46:57,063 - INFO:Done converting records to numeric
2025-10-25 11:46:57,063 - INFO:Normalizing string data to lower case
2025-10-25 11:46:57,063 - INFO:Done normalizing string data
2025-10-25 11:46:57,063 - INFO:Checking optional field to compute the value
2025-10-25 11:46:57,063 - INFO:The size of skipped ros is 3:
[{'order_id': 'ORD005', 'timestamp': '2025-10-19T08:20:00Z', 'item': '', 'quantity': 1, 'price': 45.0, 'total': 45, 'payment_status': 'refunded'}, {'order_id': 'ORD007', 'timestamp': '2025-10-19T08:30:00Z', 'item': 'power bank', 'quantity': 'N/A', 'price': 25.0, 'total': 50.0, 'payment_status': 'paid'}, {'order_id': 'ORD011', 'timestamp': '19/10/2025 08:10 AM', 'item': 'usb cable', 'quantity': 8.2, 'price': None, 'total': 20.5, 'payment_status': 'pending'}]
2025-10-25 11:46:57,063 - INFO:The size of skipped rows after checking for optional field is 1:
2025-10-25 11:46:57,063 - INFO:The size of additional rows from skipped rows 2:
2025-10-25 11:46:57,063 - INFO:Checking and removing duplicates
2025-10-25 11:46:57,063 - INFO:Done removing duplicate
2025-10-25 11:46:57,064 - INFO:Size before removing duplicate 10
2025-10-25 11:46:57,064 - INFO:Size after removing duplicate 9
2025-10-25 11:46:57,064 - INFO:The final required data with size 9 is ready!!!
2025-10-25 11:46:57,064 - INFO:Analysing loaded data
2025-10-25 11:46:57,064 - INFO:Exporting data as shoplink_cleaned.json
2025-10-25 11:46:57,066 - INFO:Exporting data as analyzer_summary.json
```

---

##  Testing
Unit tests are handled with `pytest`.

### Run All Tests
```bash
python -m pytest -v
```

If `pytest` is not installed, install it with:
```bash
pip install pytest
```

---

## Requirements

-  Python==3.13.6  
- `python-dateutil` (for parse date timestamp ) 
- `pytest==8.4.2` (for testing)
- pluggy==1.6.0 (dependency for pytest)



### Install Dependencies
```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
Python==3.13.6
pytest==8.4.2
pluggy==1.6.0
python-dateutil==2.9.0
```


