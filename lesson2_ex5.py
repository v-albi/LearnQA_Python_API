import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

parsed_json = json.loads(json_text)
json_messages = parsed_json['messages']
print(json_messages[1])


