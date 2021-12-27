import json
import os
import pprint
import sys

def main():
    arg = sys.argv[1]
    json_object = {}

    if os.path.isfile(arg):
        with open(arg) as f:
            text = f.read()
            json_object['path'] = arg

    else:
        text = arg

    json_object['text'] = text.strip()
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

if __name__ == "__main__":
    main()
