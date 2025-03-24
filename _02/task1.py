from typing import Callable  
import json

def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    data = json.loads(json_str)
    for key in required_keys:
        if key in data.keys():
            data_tokens = list(map(lambda x: x.lower(), data[key].split(" ")))
            for token in tokens:
                if token.lower() in data_tokens:
                    print(callback(key, token))


json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
required_keys = ["key1", "key2"]
tokens = ["WORD1", "word2"]
         
process_json(json_str, required_keys, tokens, lambda key, token: f"{key=}, {token=}")