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

"""dictionary = {
    '67037c00-ed18-4c60-b261-849109b71697': {
        'server1/': {
            'https://fredespresso.hubofallthings.net/api/v2.6/files/': ['file/sourcedir1fred.txt','content/sourcedir1fred.txt']
        }
    }, 
    'b1841f47-4f18-460b-b881-05d7557d0712': {
        'server1/': {
            'https://fredespresso.hubofallthings.net/api/v2.6/files/': ['file/sourcedir1fred.txt','content/sourcedir1fred.txt'],
            'https://gemmaespresso.hubofallthings.net/api/v2.6/files/': ['file/gemma.txt','content/gemma.txt']
        }, 
        'server2/': {
            'https://harryespresso.hubofallthings.net/api/v2.6/files/': ['file/harry.txt','content/harry.txt'], 
            'https://imogenespresso.hubofallthings.net/api/v2.6/files/': ['file/imogen.txt','content/imogen.txt'], 
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/jimmy.txt','content/jimmy.txt']
        }
    }, 
    '6561a0f3-ed1b-4378-bf46-c4ed190ad213': {
        'server1/': {
            'https://fredespresso.hubofallthings.net/api/v2.6/files/': ['file/sourcedir1fred.txt'], 
            'https://gemmaespresso.hubofallthings.net/api/v2.6/files/': ['file/gemma.txt']
        }, 
        'server2/': {
            'https://harryespresso.hubofallthings.net/api/v2.6/files/': ['file/harry.txt'], 
            'https://imogenespresso.hubofallthings.net/api/v2.6/files/': ['file/imogen.txt'],
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/jimmy.txt']
        }
    }, 
    'e8edfb2b-a949-4970-add7-f62907d27b3d': {
        'server1/': {
            'https://fredespresso.hubofallthings.net/api/v2.6/files/': ['file/sourcedir1fred.txt','content/sourcedir1fred.txt'], 
            'https://gemmaespresso.hubofallthings.net/api/v2.6/files/': ['file/gemma.txt']
        }
    }, 
    'bb16336a-ecdd-4c17-a77d-962bbc9aaca9': {
        'server1/': {
            'https://fredespresso.hubofallthings.net/api/v2.6/files/': ['file/sourcedir1fred.txt','content/sourcedir1fred.txt'],
            'https://gemmaespresso.hubofallthings.net/api/v2.6/files/': ['file/gemma.txt','content/gemma.txt']
        }, 
        'server2/': {
            'https://harryespresso.hubofallthings.net/api/v2.6/files/': ['file/harry.txt','content/harry.txt'],  
            'https://imogenespresso.hubofallthings.net/api/v2.6/files/': ['file/imogen.txt','content/imogen.txt'],  
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/jimmy.txt','content/jimmy.txt']
        }
    }, 
    '4bf455c4-0100-4634-a80c-6be19679e4b1': {
        'server1/': {
            'https://gemmaespresso.hubofallthings.net/api/v2.6/files/': ['file/gemma.txt','content/gemma.txt']
        }
    }, 
    '09bc9f2f-62a2-4c85-82b7-088b3cb5b528': {
        'server1/': {
            'https://gemmaespresso.hubofallthings.net/api/v2.6/files/': ['file/gemma.txt','content/gemma.txt']
        }, 
        'server2/': {
            'https://harryespresso.hubofallthings.net/api/v2.6/files/': ['file/harry.txt']
        }
    }, 
    '386f54de-7845-466c-99a6-4df87fb539ad': {
        'server2/': {
            'https://harryespresso.hubofallthings.net/api/v2.6/files/': ['file/harry.txt','content/harry.txt']
        }
    }, 
    '4ab0f763-55ba-4cd6-bab7-24d3ad66f9f9': {
        'server2/': {
            'https://harryespresso.hubofallthings.net/api/v2.6/files/': ['file/harry.txt','content/harry.txt'], 
            'https://imogenespresso.hubofallthings.net/api/v2.6/files/': ['file/imogen.txt']
        }
    }, 
    '3cb67db3-d41d-4a0f-a8ac-57359b3cc913': {
        'server2/': {
            'https://imogenespresso.hubofallthings.net/api/v2.6/files/': ['file/imogen.txt','content/imogen.txt'], 
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/jimmy.txt']
        }
    }, 
    '3427fac3-a671-4960-9503-8b7caaf1b6ab': {
        'server2/': {
            'https://imogenespresso.hubofallthings.net/api/v2.6/files/': ['file/imogen.txt','content/imogen.txt'],
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/jimmy.txt']
        }
    }, 
    '36ea0038-9e62-4cd6-b999-3381cc7551e2': {
        'server2/': {
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/stormy.txt','content/stormy.txt'], 
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/jimmy.txt','content/jimmy.txt']
        }
    }, 
    'public': {
        'server2/': {
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['file/stormy.txt','content/stormy.txt']
        }
    } 
}"""

"""dictionary = { 
    'public': {
        'server2/': {
            'https://jimmyespresso.hubofallthings.net/api/v2.6/files/': ['/file/stormy.txt','/content/stormy.txt']
        }
    } 
}"""

# HO 08/07/2025 BEGIN ******
# Convert dictionary to JSON string
#dictionary_json = json.dumps(dictionary)
# Index.jar expects a file path
dictionary_json = 'testdataswyft.json'
# HO 08/07/2025 END ******

# Specify source and output directories
source_dir = "Dataswyfttestsource"
output_dir = "Dataswyfttestsink"

# Path to the JAR file
jar_file = "Index.jar"

# Run the Java program with the JAR file
result = subprocess.run([
    "java", "-jar", jar_file, dictionary_json, source_dir, output_dir
], capture_output=True, text=True)

# Print the output from the Java program
print(result.stdout)
print(result.stderr)  # If there were any errors