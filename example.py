import json

ordered_dict = {"first": 1, "second": 2, "third": 3}

json_string = json.dumps(ordered_dict)

print(json_string)