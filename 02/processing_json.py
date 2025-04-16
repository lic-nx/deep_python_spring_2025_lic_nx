from typing import Callable
import json


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    if len(json_str) < 1:
        return
    data = json.loads(json_str)
    for key in required_keys:
        if key in data.keys():
            data_tokens = list(map(lambda x: x.lower(), data[key].split(" ")))
            for token in tokens:
                count = data_tokens.count(token.lower())
                for _ in range(count):
                    callback(key, token)
