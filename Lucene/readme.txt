Python usage:

import subprocess
import json

# Sample access control data with lists of web IDs
access_control = {
    "file1.txt": ["webId1", "webId2"],
    "file2.txt": ["webId3"]
}

# Convert the dictionary to a JSON string
access_control_data = json.dumps(access_control)

command = [
    'java',
    '-jar',
    'Indexer.jar',  # Path to your JAR file
    '/users/thanassis/Documents/Files',  # Path to the files to index
    access_control_data,  # Pass the JSON string with lists of web IDs
    '/users/thanassis/Documents/Index'  # Path for the destination index
]

# Run the command
result = subprocess.run(command, capture_output=True, text=True)

# Output the result
print(result.stdout)
print(result.stderr)
