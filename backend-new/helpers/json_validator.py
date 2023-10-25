from referencing import Registry, Resource
import os, json, referencing.jsonschema
from jsonschema import Draft202012Validator

SCHEMA_DIR = os.path.abspath("backend-new/schemas")#TODO: change it to "schemas"


def list_files_recursively(dir:str, list:[str], base_path=SCHEMA_DIR)->[str]:
    for f in os.scandir(dir):
        path = os.path.join(base_path, f.name)
        if f.is_dir():
            list_files_recursively(f, list, path)
        if f.is_file():
            list.append(path)
    return list


class JSONValidator():

    def __init__(self):
        schema_files = list_files_recursively(SCHEMA_DIR, [])
        self.schemas = dict()
        self.validators = dict()
        self.registry = Registry()

        for i in schema_files:
            json_file = open(i, 'r')
            json_data = json.loads(json_file.read())
            self.schemas[json_data["title"]] = json_data
            self.registry = Resource(json_data, specification=referencing.jsonschema.DRAFT202012) @ self.registry
            json_file.close()

        for i in self.schemas:
            self.validators[i] = Draft202012Validator(schema=self.schemas[i], registry=self.registry)