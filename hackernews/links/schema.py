import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


#define your mutation class

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()


# the kind of data in the server

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate (self,info,url,description):
    link = Link(url=url, description=description)
    link.save()

    return CreateLink(
        id= link.id
        url = link.url
        description = link.description
    )


#points to created mutation

class Mutation(graphene.ObjectType):
    create_link = CreateLink()