import strawberry
@strawberry.type(description="""Root query""")
class Query:

    from .PreferenceTagGQLModel import preference_tags

    from .PreferenceTagGQLModel import preference_tag_by_id

    from .PreferenceTagGQLModel import preference_tags_page

    #############################################################
    #
    # Tag entities
    #
    #############################################################

    from .PreferenceTagEntityGQLModel import preference_entities_labeled
 
    from .PreferenceTagEntityGQLModel import preference_entity_types

    from .PreferenceTagEntityGQLModel import preference_tags_for_entity


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

    from .PreferenceUserSettingsGQLModel import preference_settings_user_page

    from .PreferenceUserSettingsGQLModel import preference_settings_user_in_type


    
    pass