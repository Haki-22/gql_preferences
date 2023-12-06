import strawberry

@strawberry.type
class Mutation:
    
    from .TagGQLModel import tag_insert
    tag_insert = tag_insert

    from .TagGQLModel import tag_update
    tag_update = tag_update

    from .TagGQLModel import tag_delete
    tag_delete = tag_delete

    from .TagEntityGQLModel import tag_add_to_entity
    tag_add_to_entity = tag_add_to_entity

    from .TagEntityGQLModel import tag_remove_from_entity
    tag_remove_from_entity = tag_remove_from_entity

    #############################################################
    #
    # Preference Settings Type
    #
    #############################################################

    from .PreferenceSettingsTypeGQLModel import preference_settings_type_insert
    preference_settings_type_insert = preference_settings_type_insert
    
    from .PreferenceSettingsTypeGQLModel import preference_settings_type_update
    preference_settings_type_update = preference_settings_type_update

    from .PreferenceSettingsTypeGQLModel import preference_settings_type_delete
    preference_settings_type_delete = preference_settings_type_delete

    #############################################################
    #
    # Preference Settings 
    #
    #############################################################

    from .PreferenceSettingsGQLModel import preference_settings_insert

    from .PreferenceSettingsGQLModel import preference_settings_update

    from .PreferenceSettingsGQLModel import preference_settings_delete

    #############################################################
    #
    # User settings 
    #
    #############################################################

    from .UserSettingsGQLModel import preference_user_settings_type_insert

    from .UserSettingsGQLModel import preference_user_settings_type_update

    from .UserSettingsGQLModel import preference_user_settings_delete

    pass