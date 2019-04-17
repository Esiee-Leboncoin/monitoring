from wtforms import Form, StringField, SelectField, SubmitField
from utils import bdd, pipelines
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

class PipelineSelectEditor(Form):
    display = SubmitField(label='Afficher')
    delete = SubmitField(label='Supprimer')
    all_pipes = pipelines.get_all_pipes_names("static/pipelines")
    all_pipes = [(g[:-3], g[:-3]) for g in pipelines.get_all_pipes_names("static/pipelines")]
    pipToEdit = SelectField(choices = all_pipes)

def UpdateEditor(form):
    form.pipToEdit.choices = [(g[:-3], g[:-3]) for g in pipelines.get_all_pipes_names("static/pipelines")]

def UpdateGraph(form, field):
    all_collections = mongo.db.collection_names()
    if ("users" in all_collections):
        all_collections.remove("users")
    form[field].choices = [(g, g) for g in all_collections]


