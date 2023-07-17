# Finsure tech challenge

## Requirements
The following requirements were implemented as per the original request:
1. Create a new Lender 
1. List all Lenders (five per page) 
   - List active lenders 
1. Get a specific Lender 
1. Update a specific Lender 
1. Delete a specific Lender 
1. Bulk upload Lenders in CSV format 
1. Download Lenders in CSV format

## How to install
You can use any virtual environment and use requirements.txt to pull all the required packages.
Here is an example using **virtualenv**:
```
python -m venv env
. env/scripts/activate
pip install -r requirements.txt
```

Please also update your database configs via settings.py **DATABASES** and run migrations before starting the server.

## How to use and payload examples
You can start by creating some dummy data via the CSV upload endpoint (using the lenders.csv file).
Default upload URL: http://127.0.0.1:8000/lenders/csv/?csv_file=[your_file]
**Please not that as CSV endpoints are not part of the JSON:API spec, please use a standard Content-Type when making your requests**

BrowsableAPIRenderer can also be enabled for easier testing.

Available urls:
Create a new Lender: http://127.0.0.1:8000/lenders/ (POST). **Please make sure to use application/vnd.api+json Content-Type as per JSON:API spec**. Example payload:
```
{
    "data": {
        "type": "Lender",
        "attributes": {
            "name": "Test User",
            "code": "asf",
            "trial_commission_rate": 99,
            "active": True,
            "upfront_commission_rate": 22
        }
    }
}
```
List all lenders: http://127.0.0.1:8000/lenders/ (GET)
List all active lenders: http://127.0.0.1:8000/lenders/?filter[active]=true
Retrieve a lender: http://127.0.0.1:8000/lenders/[id]/ (GET)
Update a specific lender: http://127.0.0.1:8000/lenders/[id]/ (PATCH or PUT). Example PATCH payload:
```
{
    "data": {
        "type": "Lender",
        "id": [id]
        "attributes": {
            "code": "123"
        }
    }
}
```
Delete a specific lender: http://127.0.0.1:8000/lenders/[id]/ (DELETE)
Download lenders as CSV: http://127.0.0.1:8000/lenders/csv/ (GET)

## Assumptions and implementation
Given the "intentionally sparse" requirements, the following things were considered:
* There is no requirements for data uniqueness, thereby, data duplicates are possible
* Some basic validation was added:
  - Code can contain only up to 3 symbols
  - Percentage values are expected in the xx.xx format (up to 2 decimal points, simple integers will work as well)
  - Perecentage values can be only in [0, 100] range
* There is no detailed API:JSON specs for bulk updates via CSV so all the CSV endpoints return some basic responses
* CSV creation endpoint will provide some basic feedback (validation):
  - All the successful creations will be listed in the "success" object containing the basic object data
  - Any errors will be listed in the "errors" object with detailed serialization response
* Some very basic testing was added as well

