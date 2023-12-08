import strawberry

@strawberry.type
class Mutation:
   
    #############################################################
    #
    #  Tag Model
    #
    #############################################################    

    from .PreferenceTagGQLModel import tag_insert

    from .PreferenceTagGQLModel import tag_update

    from .PreferenceTagGQLModel import tag_delete

    #############################################################
    #
    # Tag entities
    #
    #############################################################

    from .PreferenceTagEntityGQLModel import tag_add_to_entity

    from .PreferenceTagEntityGQLModel import tag_remove_from_entity

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

    from .PreferenceUserSettingsGQLModel import preference_user_settings_type_insert

    from .PreferenceUserSettingsGQLModel import preference_user_settings_type_update

    from .PreferenceUserSettingsGQLModel import preference_user_settings_delete

    pass