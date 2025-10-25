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

## 🧩 Example Usage

### 1. Run the Pipeline
```bash
python -m order_pipeline.pipeline
```

### 2. Example Data (input.json)
```json
[
  {
    "order_id": "ORD001",
    "timestamp": "19/10/2025 08:10 AM",
    "item": "USB Cable",
    "quantity": "2",
    "price": "5.5",
    "total": "11.0",
    "payment_status": "Paid"
  }
  {
    "order_id": "ORD002", 
    "timestamp": "2025-10-19T08:00:00Z",
    "item": "Wireless Mouse", 
    "quantity": 2, 
    "price": "$15.99",
    "total": "$31.98",
    "payment_status": "paiD"
    },
{
  "order_id": "ORD003", 
  "timestamp": "2025-10-19 08:05",
  "item": "Laptop Sleeve",
  "quantity": "1",
  "price": "N12.50",
  "total": "$12.50",
  "payment_status": "PAID"  
  },
{
  "order_id": "ORD004", 
  "timestamp": "2025-10-19T08:00:00Z",
  "item": "Wireless Mouse", 
  "quantity": 4, 
  "total": "$31.98"
},
{
  "order_id": "ORD005", 
  "timestamp": "19/10/2025 08:10 AM",
  "item": "USB Cable", 
  "quantity": None, 
  "price": "N2.5", 
  "total": "$20.50", 
  "payment_status": "pending" 
}
]
```

### 3. Example Output (console/log)
```
INFO: Reading data from file...
INFO: Validating and cleaning 10 records...
INFO: Transforming timestamps and recalculating totals...
INFO: Total revenue: 1050.50
INFO: Average revenue: 87.54
INFO: Payment summary: {'paid': 9, 'pending': 1}
```

---

## 🧪 Testing
Unit tests are handled with `pytest`.

### Run All Tests
```bash
pytest -v
```

If `pytest` is not installed, install it with:
```bash
pip install pytest
```

---

## 🧰 Requirements

- Python ≥ 3.8  
- `python-dateutil`  
- `pytest` (for testing)

### Install Dependencies
```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
python-dateutil
pytest
```

---

## 🕓 Timestamp Standardization
The transformer normalizes timestamps to **ISO 8601 UTC format**:
```
2025-10-19T08:15:00Z
```
It handles different input formats such as:
- `19/10/2025 08:10 AM`
- `2025-10-19 08:15`

---

## 🧑‍💻 Author
Developed by **Oluwaseyi** — as part of a data engineering and analytics workflow project.

---

## 🧱 Future Enhancements
- Support for CSV and Excel inputs.  
- Integration with SQL databases for export.  
- Stream-based processing using Kafka or Spark.  
- CLI options for configuration and logging level.  

---

## 🏁 License
MIT License © 2025 Oluwaseyi
