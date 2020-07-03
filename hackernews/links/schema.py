import graphene
from graphene_django import DjangoObjectType
from ghraphql import GraphQLError
from django.db.models import Q

from .models import Link, Vote


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    # Add the first and skip parameters
    links = graphene.List(
        LinkType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)

    # Use them to slice the Django queryset
    def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Link.objects.all()

        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


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



class CreateVote(graphene.Mutation):
    user=graphene.Field(UserType)
    link= graphene.Fiels(LinkType)

    class Arguments :
        link_id =graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('rafiki login to vote')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Rafiki the lnk is invalid')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()