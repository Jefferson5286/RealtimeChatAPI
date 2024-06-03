from typing import Dict, List, Any
from orjson import loads


class OpenAPI:
    def __init__(self):
        with open('./OpenAPI.json', 'r', encoding='utf-8') as file:
            data = loads(file.read())

        self.title: str = data['info']['title']
        self.description: str = data['info']['description']
        self.version: str = data['info']['version']

        self.serves: List[Dict[str, str]] = data['servers']
        self.paths: Dict[str, Any] = data['paths']

        del data

    def get_responses(self, method: str, path: str):
        return self.paths.get(path).get(method)['responses']


openapi = OpenAPI()
