# Flow Log Parser README
## Introduction
The program is designed to parse flow log data, map each row to a tag based on a lookup table, and generate counts of matches for each tag and port/protocol combination. This README covers the assumptions made during development, instructions on how to compile and run the program, tests performed, and additional analysis of the code.

----
----

## Assumptions Made
The following assumptions were made while developing the program:

1. Default Log Format Support: The program only supports the default flow log format, not custom formats.
1. Flow Log Version: Only version 2 of the flow logs is supported.
1. Plain Text Files: Both the flow log file and the lookup table file are assumed to be plain text (ASCII) files.
1. File Sizes:
    -  The flow log file size can be up to 10 MB.
    - The lookup table can have up to 10,000 mappings.
1. Case Insensitivity:
    - Matching of protocols and tags is case-insensitive.
    - Protocol names in the lookup table and flow logs are normalized to lowercase.
1. Protocol Support:
    - The program maps protocol numbers to names for TCP (6), UDP (17), and ICMP (1).
    - Unrecognized protocol numbers are labeled as 'unknown'.
1. Flow Log Fields:
    - The program expects each flow log entry to have at least 14 fields.
    - Lines with fewer fields are considered malformed and are skipped.
1. Destination Port for Mapping:
    - The mapping to tags is based on the destination port and protocol.
1. Counting Untagged Entries:
    - Flow log entries that do not match any mapping in the lookup table are counted under the tag 'Untagged'.

----
----

## Program Overview
The Flow Log Parser performs the following steps:

1. Load the Lookup Table:
    - Reads the lookup table CSV file.
    - Stores mappings of (destination port, protocol) to tag in a dictionary.
1. Process Flow Logs:
    - Reads the flow log file line by line.
    - Extracts the destination port and protocol number from each entry.
    - Converts the protocol number to a protocol name (tcp, udp, icmp).
    - Looks up the tag based on the destination port and protocol.
    - Counts matches for each tag and port/protocol combination.
1. Generate Output:
    - Prints counts of matches for each tag.
    - Prints counts of matches for each port/protocol combination.

----
----

## Instructions on How to Compile/Run the Program
### Prerequisites
- Python 3.6 or higher installed on your system.
- Basic knowledge of using the command line.
### Program Files
- `main.py`: The main program file.
- `flowlog.txt`: The flow log data file.
- `lookup.csv`: The lookup table CSV file.
- `output.txt`: The output file (saved in same directory of main.py).

### Steps to Run the Program
#### Prepare Input Files
- Flow Log File: Save your flow log data into a text file, e.g., flowlog.txt.
Lookup Table CSV File: Save your lookup table into a CSV file, e.g., lookup.csv. Ensure it has the columns `dstport`, `protocol`, and `tag`.
Run the Program
- Open a terminal or command prompt.
- Navigate to the directory containing main.py.

#### Run the following command:
```
    python main.py flowlog.txt lookup.csv
```

> Replace `flowlog.txt` and `lookup.csv` with the paths to your actual files if they are named differently.

#### Review the Output
- The program will print the counts of matches for each tag and for each port/protocol combination.

----
----

## Tests Performed
Several tests were conducted to ensure the program works as intended:

#### Test 1: Sample Data Test
- Purpose: Validate the program using the provided sample flow logs and lookup table.
- Steps:
  - Used the sample flow logs and lookup table provided in the initial requirements.
  - Ran the program and verified that the output matches the expected results.
- Result: The program correctly counted the matches for each tag and port/protocol combination as per the sample output.
#### Test 2: Large Lookup Table Test
- Purpose: Test the program's ability to handle a lookup table with 10,000 mappings.
- Steps:
  - Generated a lookup table CSV file with 10,000 random port/protocol/tag mappings.
  - Ran the program with a flow log file containing entries that match some of these mappings.
- Result: The program successfully loaded the large lookup table and processed the flow logs without any performance issues.
#### Test 3: Large Flow Log File Test
- Purpose: Ensure the program can handle a flow log file up to 10 MB in size.
- Steps:
  - Created a flow log file approximately 10 MB in size with various entries.
  - Ran the program and measured the execution time and memory usage.
- Result: The program processed the large flow log file efficiently, with acceptable execution time and low memory consumption.
#### Test 4: Case Insensitivity Test
- Purpose: Verify that the matching is case-insensitive.
- Steps:
  - Modified the lookup table and flow log entries to use mixed-case protocol names and tags.
  - Ran the program to check if it correctly matches entries regardless of case.
- Result: The program correctly matched entries in a case-insensitive manner.
#### Test 5: Unsupported Protocol Test
- Purpose: Test how the program handles flow logs with unsupported protocol numbers.
- Steps:
  - Added flow log entries with protocol numbers not mapped in the `protocolNumberToName` function.
  - Ran the program to see how it labels these protocols.
- Result: The program labeled unknown protocols as 'unknown' and included them in the counts.

----
----

## Additional Analysis and Notes
### Performance Analysis
- Memory Usage: The program has a low memory footprint due to line-by-line processing of the flow log file and efficient use of data structures.
- Execution Time: The program executes quickly, even with large input files, thanks to the use of dictionaries for constant-time lookups.
### Extensibility
- Protocol Mapping: The `protocolNumberToName` function can be extended to support additional protocols by adding new entries to the mapping dictionary.
- Error Handling: The program skips malformed lines and continues processing, ensuring robustness.
### Data Structures
- Lookup Dictionary: Stores port/protocol combinations as keys and tags as values. Suitable for up to 10,000 mappings with minimal memory usage (~1 MB).
- Default Dictionaries: Used for counting tags and port/protocol combinations efficiently.
### Code Readability
- Modular Design: Functions are used to separate concerns (`loadLookupTable`, `parseFlowLog`, `mapTags`, `writeOutput`, `protocolNumberToName`, and `main`).
- Comments: Inline comments explain key steps, improving code readability.
### Potential Enhancements
- Logging: Adding logging statements could help in debugging and monitoring the program's execution.
- Configuration File: Using a configuration file for parameters like file paths could make the program more flexible.
- Command-Line Arguments: Enhancing argument parsing to include optional parameters (e.g., output file, verbosity level).

----
----

## Conclusion
The Flow Log Parser program meets the specified requirements and efficiently processes flow logs to map entries to tags based on a lookup table. By adhering to the assumptions and following the instructions provided, users can successfully run the program and obtain the desired output.

----
----
----