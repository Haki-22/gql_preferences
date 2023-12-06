import datetime
from functools import cache
from aiodataloader import DataLoader
from sqlalchemy import select, update

from uoishelpers.dataloaders import createIdLoader

from gql_preferences.DBDefinitions import (
    TagModel, 
    TagEntityModel,

    PreferenceSettingsTypeModel,
    PreferenceSettingsModel,
    UserSettingsModel
)

dbmodels = {
    "tags": TagModel,
    "tagentities" : TagEntityModel,
    "preference_settings_types" : PreferenceSettingsTypeModel,
    "preference_settings": PreferenceSettingsModel,
    "user_settings": UserSettingsModel,
}

def createDataLoders(asyncSessionMaker, models=dbmodels):
    result = createLoaders(asyncSessionMaker, models)
    return result


async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

# Function to get loaders from the GraphQL context
def getLoaders(info):
    return info.context["all"]

# Function to get the user from the GraphQL context
def getUser(info):
    return info.context["user"]
