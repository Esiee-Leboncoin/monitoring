from wtforms import Form, StringField, SelectField
from utils import bdd

mongo = bdd.MongoDB("database_pipeline")

class FirstGraphSelection(Form):
    all_collections = mongo.db.collection_names()
    if ("users" in all_collections):
        all_collections.remove("users")
    myChoices = [(g, g) for g in all_collections]
    myField = SelectField(u'Field name', choices = myChoices)

class SecondGraphSelection(Form):
    all_collections = mongo.db.collection_names()
    if ("users" in all_collections):
        all_collections.remove("users")
    myChoices = [(g, g) for g in all_collections]
    myField2 = SelectField(u'Field name', choices = myChoices)

class ThirdGraphSelection(Form):
    all_collections = mongo.db.collection_names()
    if ("users" in all_collections):
        all_collections.remove("users")
    myChoices = [(g, g) for g in all_collections]
    myField3 = SelectField(u'Field name', choices = myChoices)

class FourthGraphSelection(Form):
    all_collections = mongo.db.collection_names()
    if ("users" in all_collections):
        all_collections.remove("users")
    myChoices = [(g, g) for g in all_collections]
    myField4 = SelectField(u'Field name', choices = myChoices)

class PipelineToAnalyse(Form):
    all_collections = mongo.db.collection_names()
    if ("users" in all_collections):
        all_collections.remove("users")
    myChoices = [(g, g) for g in all_collections]
    pipelineToAnalyse = SelectField(u'Field name', choices = myChoices)
