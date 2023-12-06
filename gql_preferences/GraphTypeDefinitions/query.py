import strawberry
@strawberry.type(description="""Root query""")
class Query:

    from .TagEntityGQLModel import preference_entities
    preference_entities = preference_entities
    
    from .TagGQLModel import preference_tags
    preference_tags = preference_tags
    
    from .TagEntityGQLModel import preference_entity_tags
    preference_entity_tags = preference_entity_tags

    from .TagGQLModel import tag_by_id
    tag_by_id = tag_by_id

    #############################################################
    #
    # Preference Settings Type
    #
    #############################################################

    from .PreferenceSettingsTypeGQLModel import preference_settings_type_page
    preference_settings_type_page = preference_settings_type_page

    from .PreferenceSettingsTypeGQLModel import preference_settings_type_by_id
    preference_settings_type_by_id = preference_settings_type_by_id

    from .PreferenceSettingsTypeGQLModel import preference_settings_default_by_type_id

    #############################################################
    #
    # Preference Settings 
    #
    #############################################################

    from .PreferenceSettingsGQLModel import preference_settings_page

    from .PreferenceSettingsGQLModel import preference_settings_by_id

    #from .PreferenceSettingsGQLModel import user_settings_page

    #from .PreferenceSettingsGQLModel import preference_settings_default_page

    """ from .PreferenceSettingsGQLModel import preference_settings_default_by_type_id """

    #############################################################
    #
    # User settings 
    #
    #############################################################

    from .UserSettingsGQLModel import preference_settings_user_page

    from .UserSettingsGQLModel import preference_settings_user_in_type


    
    pass