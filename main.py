import csv
import sys
from collections import defaultdict

'''
https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
srcport: parts[5]
dstport: parts[6]
protocol: parts[7]
'''

# Load lookup table
def loadLookupTable(filename):
    lookupTable = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract destination port, protocol and tag
            dstPort = row['dstport'].strip().lower()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()

            # Add to lookup table
            lookupTable[(dstPort, protocol)] = tag
    return lookupTable

# Map protocol number to name
def protocolNumberToName(protocolNumber, unrecognised='unknown'):
    mapping = {
        '6': 'tcp',
        '17': 'udp',
        '1': 'icmp',
    }
    return mapping.get(protocolNumber, unrecognised)

# Parse flow log
def parseFlowLog(filename):
    flowLogs = []
    with open(filename, mode='r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 14:
                # Skip malformed lines
                print("Skipping malformed line:", line)
                continue

            # Extract destination port and protocol
            dstPort = parts[6].lower()
            protocolNumber = parts[7]
            protocol = protocolNumberToName(protocolNumber).lower()

            # Add to flow logs
            flowLogs.append((dstPort, protocol))
    return flowLogs

# Map tags and count occurrences
def mapTags(flowLogs, lookupTable):
    tagCounts = defaultdict(int)
    portProtocolCounts = defaultdict(int)

    # Count occurrences of each tag and port/protocol combination
    for dstPort, protocol in flowLogs:
        key = (dstPort, protocol)
        tag = lookupTable.get(key, 'Untagged')

        # Increment tag count
        tagCounts[tag] += 1

        # Increment port/protocol count
        portProtocolCounts[key] += 1

    return tagCounts, portProtocolCounts

# Write output to file
def writeOutput(tagCounts, portProtocolCounts, outputFile):
    with open(outputFile, mode='w') as file:

        # Write tag counts
        file.write("# Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tagCounts.items():
            file.write(f"{tag},{count}\n")
        
        # Write port/protocol counts
        file.write("\n-----\n# Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (dstPort, protocol), count in portProtocolCounts.items():
            file.write(f"{dstPort},{protocol},{count}\n")

# Main function
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python main.py <flow_log_file> <lookup_table_file>")
        sys.exit(1)

    print("Processing flow logs...")
    print(sys.argv)
    # Load lookup table and parse flow log
    flowLogsFile = sys.argv[1]
    lookupTableFile = sys.argv[2]

    flowLogs = parseFlowLog(flowLogsFile)
    lookupTable = loadLookupTable(lookupTableFile)
    outputFile = "output.txt"

    # Map tags and count occurrences
    tagCounts, portProtocolCounts = mapTags(flowLogs, lookupTable)

    # Write output to file
    writeOutput(tagCounts, portProtocolCounts, f'{outputFile}')

    print(f'Processing complete. Output written to "{outputFile}".')
