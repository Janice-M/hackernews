import graphene

from graphene_django import DjangoObjectType

#schema importations

from .models import Link 

class LinkType(DjangoObjectType)
    class Meta:
        model = link


class Query (graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links (self, info, **kwargs):
        