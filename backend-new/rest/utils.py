import abc,inspect,os,json
from collections import OrderedDict
from rest_framework import serializers
from django.db import models
from jsonschema import ValidationError,Draft7Validator

class JSONModelMeta(abc.ABCMeta, type(models.Model)):
    def __new__(cls, name, bases, attrs):
        klass = super().__new__(cls, name, bases, attrs)
        klass.json = models.JSONField(default=dict)
        if not inspect.isabstract(klass):
            klass.validator = ValidatorManager.get_instance().validators[attrs['schema_title']]
        return klass

class JSONModelSerializerMeta(abc.ABCMeta, type(serializers.Serializer)):
    def __new__(cls, name, bases, attrs):
        klass = super().__new__(cls, name, bases, attrs)
        klass.json = serializers.JSONField()
        if not inspect.isabstract(klass):
            schema_title = attrs['schema_title']
            def validate_json(self, value):
                if isinstance(value, str):
                    value = json.loads(value)
                try:
                    self.validate(value)
                except ValidationError as e:
                    raise serializers.ValidationError("The data is not compatible with given format.") from e
                return value
            klass.validate_json = validate_json
        return klass


class JSONModel(models.Model, metaclass=JSONModelMeta):
    json = models.JSONField(default=dict)
    class Meta:
        abstract=True
    
    @property
    @abc.abstractclassmethod
    def schema_title():
        pass

    @property
    @abc.abstractclassmethod
    def serializer_class():
        pass

class JSONModelSerializer(serializers.Serializer, metaclass=JSONModelSerializerMeta):

    @property
    @abc.abstractstaticmethod
    def schema_title():
        pass

    def to_representation(self, obj):
        if isinstance(obj.json, list):
            return obj.json
        return OrderedDict(obj.json)

class ValidatorManager():
    """
    A singleton class to manage all validators that resides in schemas directory

    Attributes
    ----------
    schemas : dict[str, 'json']
        type-name -> schema
    validators : dict[str, Draft7Validator]
        type-name -> validator
    """
    __instance = None
    __SCHEMA_DIR = os.path.abspath("rest/schemas")

    @classmethod
    def get_instance(Self)->'ValidatorManager':
        if Self.__instance == None:
            ValidatorManager()
        return Self.__instance

    def __new___(cls, *args, **kwargs):
        if cls.__instance != None:
            return cls.__instance

    def __init__(self):
        if ValidatorManager.__instance != None:
            raise Exception("ValidatorManager is already instantiated!")
        
        schema_files = list_files_recursively(ValidatorManager.__SCHEMA_DIR, [], ValidatorManager.__SCHEMA_DIR)
        self.schemas = dict()
        self.validators = dict()

        for i in schema_files:
            json_file = open(i, 'r')
            json_data = json.loads(json_file.read())
            self.schemas[json_data["title"]] = json_data
            self.validators[json_data["title"]] = Draft7Validator(json_data)
            json_file.close()
        ValidatorManager.__instance = self

def list_files_recursively(dir:str, list:[str], base_path)->[str]:
    for f in os.scandir(dir):
        path = os.path.join(base_path, f.name)
        if f.is_dir():
            list_files_recursively(f, list, path)
        if f.is_file():
            list.append(path)
    return list
