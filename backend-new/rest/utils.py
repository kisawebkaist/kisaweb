import abc,inspect,os,json
from collections import OrderedDict
from typing import Optional, Union
from rest_framework import serializers
from django.db import models
from jsonschema import ValidationError,Draft7Validator

class JSONModelMeta(abc.ABCMeta, type(models.Model)):

    def __new__(cls, name, bases, attrs):
        klass = super().__new__(cls, name, bases, attrs)
        if not inspect.isabstract(klass):
            klass.validator = ValidatorManager.get_instance().validators[attrs['schema_title']]
        return klass

class JSONModelSerializerMeta(abc.ABCMeta):
    
    def __new__(cls, name, bases, attrs):
        klass = super().__new__(cls, name, bases, attrs)

        if not inspect.isabstract(klass):
            attrs['model_class'].serializer_class = klass
        return klass

class JSONModel(models.Model, metaclass=JSONModelMeta):
    """
    A abstract django model for json storage

    Mandatory Class Atttributes
    ----------------------------
    - schema_title : the title of the json-schema for validation
    deployed_pk : the pk of the deployed json

    Extra Class Methods
    -------------------
    - get_deployed(cls)
    """

    json = models.JSONField(default=dict)
    class Meta:
        abstract=True

    @classmethod
    def get_deployed(cls):
        """
        returns the deployed object
        """
        return cls.objects.filter(pk=cls.deployed_pk)[0]
    
    @property
    @abc.abstractclassmethod
    def schema_title():
        pass

    @property
    @abc.abstractclassmethod
    def deployed_pk():
        pass

class JSONModelSerializer(serializers.BaseSerializer, metaclass=JSONModelSerializerMeta):
    """
    An ABC for making serializers for `JSONModel`.

    Upon creation of a subclass, it will add a class attribute `serializer_class` to the corresponding `JSONModel`

    Mandatory Class Attributes
    ---------------------------
    model_class : `JSONModel`
        the `JSONModel` class which this class serializes
    """
    @property
    @abc.abstractclassmethod
    def model_class()->JSONModel:
        pass

    def to_representation(self, obj):
        return obj.json
    
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        print(data)
        try:
            self.model_class.validator.validate(data)
        except ValidationError as e:
            raise serializers.ValidationError(detail=e.message, code='invalid')
        return {'json': data}
    
    def create(self, validated_data):
        return self.model_class.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.json = validated_data.json
        instance.save()
        return instance()

class ValidatorManager():
    """
    A singleton class to manage all validators that resides in schemas directory

    Attributes
    ----------
    schemas : `dict[str, 'json']`
        resolves type-name -> schema
    validators : `dict[str, Draft7Validator]`
        resolves type-name -> validator
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
        
        schema_files = list_files_recursively(dir=ValidatorManager.__SCHEMA_DIR, list=[])
        self.schemas = dict()
        self.validators = dict()

        for i in schema_files:
            with open(i, 'r') as json_file:
                json_data = json.loads(json_file.read())
                self.schemas[json_data["title"]] = json_data
                self.validators[json_data["title"]] = Draft7Validator(json_data)
        ValidatorManager.__instance = self

def list_files_recursively(dir:str, list:list[str], base_path:Optional[str]=None)->list[str]:
    """
    returns a list of all files in `dir` and its subdirectories
    """
    if base_path == None:
        base_path = dir
    for f in os.scandir(dir):
        path = os.path.join(base_path, f.name)
        if f.is_dir():
            list_files_recursively(f, list, path)
        if f.is_file():
            list.append(path)
    return list

def get_ordered_version(obj:Union[list, dict, OrderedDict]):
    """
    returns an ordered version of an json object
    """
    if isinstance(obj, list):
        return [get_ordered_version(x) for x in obj]
    if isinstance(obj, dict):
        return OrderedDict({k:get_ordered_version(v) for k,v in obj.items()})
    if isinstance(obj, OrderedDict):
        for key, value in obj.items():
            obj[key] = get_ordered_version(value)
    return obj