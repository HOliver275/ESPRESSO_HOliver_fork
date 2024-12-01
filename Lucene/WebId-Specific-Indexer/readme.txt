import subprocess
import json

# Sample dictionary (use your actual data structure)
dictionary = {
    "webid1": {
        "srv03812": {
            "pod1": ["AlecFile.txt", "AlphaFile.txt"],
            "pod2": ["Jamal.txt"]
        },
        "srv03813": {
            "pod4": ["Toer.txt"]
        }
    },
    "webid2": {
        "srv03812": {
            "pod3": ["Mo.txt", "Helen.txt"]
        }
    }
}

# Convert dictionary to JSON string
dictionary_json = json.dumps(dictionary)

# Specify source and output directories
source_dir = "/Users/thanassis/Documents/Files"
output_dir = "/Users/thanassis/Documents/Index"

# Path to the JAR file
jar_file = "Index.jar"

