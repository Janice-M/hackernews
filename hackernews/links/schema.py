import graphene
from graphene_django import DjangoObjectType

from .models import Link, Vote


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


#define your mutation class

# ...code
#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field (UserType)

    #2
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3
    def mutate(self, info, url, description):
        user= info.contex.user or None

        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by = link.posted_by
        )


#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()


class CreateVote(graphene.Mutation):
    user=graphene.Field(UserType)
    link= graphene.Fiels(LinkType)

    class Arguments :
        link_id =graphene.Int()