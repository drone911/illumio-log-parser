# illumio-log-parser

## How to run
1. Without specifying output file names.  
  ```
  python main.py path-to-flow-log path-to-lookup
  ```
2. With specifying output file names.  
  ```
  python main.py -tc /path/to/tag/count -pc /path/to/port-protocol/count path/to/flow/log path/to/lookup
  ```
  or  
  ```
  python main.py --tag_count_path /path/to/tag/count --port_protocol_count_path /path/to/port-protocol/count path/to/flow/log path/to/lookup
  ```
3. Running tests 
```
python test.py
```

## Test Outputs
```test.py``` randomly generates flow and lookup records, and shows the time taken by the aggregate logs function.  
1. For 100,000 records (10MB) in flow and 10,000 records in lookup:
<p align="center">
  <img src="https://github.com/drone911/illumio-log-parser/blob/main/img/test-output-100000-flow-10000-lookups.PNG?raw=true" />
</p>
2. For 1,000,000 records (100MB) in flow and 10,000 records in lookup:
<p align="center">
  <img src="https://github.com/drone911/illumio-log-parser/blob/main/img/test-output-1000000-flow-10000-lookups.PNG?raw=true" />
</p>
3. Generated flow and lookup files for these 2 test cases:
<p align="center">
  <img src="https://github.com/drone911/illumio-log-parser/blob/main/img/test-file-sizes.PNG?raw=true" />
</p>
