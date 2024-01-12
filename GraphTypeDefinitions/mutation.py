import strawberry

@strawberry.type
class Mutation:
   
    #############################################################
    #
    #  Tag Model
    #
    #############################################################    

    from .PreferenceTagGQLModel import preference_tag_insert

    from .PreferenceTagGQLModel import preference_tag_update

    from .PreferenceTagGQLModel import preference_tag_delete

    #############################################################
    #
    # Tag entities
    #
    #############################################################

    from .PreferenceTagEntityGQLModel import preference_tag_add_to_entity

    from .PreferenceTagEntityGQLModel import preference_tag_remove_from_entity

    #############################################################
    #
    # Preference Settings Type
    #
    #############################################################

    from .PreferenceSettingsTypeGQLModel import preference_settings_type_insert
 
    from .PreferenceSettingsTypeGQLModel import preference_settings_type_update

    from .PreferenceSettingsTypeGQLModel import preference_settings_type_delete

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