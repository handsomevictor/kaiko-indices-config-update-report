This little project aims at providing a simple way to generate a report that includes the differences between old
config.json and new config.json

## How to use it
In terminal, change directory to the project folder, then run the following command:
```
python3 generate_report.py -o indices_new.json -n indices_old.json -r summary_report.csv
```

reminder:
1. Fixings and real time configs are seperated and in a sorted way in the report.
2. Only contains Public Rates (starting with KK, having LDN etc. at the end or not), 
   things like "kaiko-gemini-btc" will not be considered
