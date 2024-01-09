import strawberry

from .query import Query
from .mutation import Mutation
from .externals import UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel

schema = strawberry.federation.Schema(Query, types=(UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel), mutation=Mutation)
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################