import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote

#1
class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']

    #2
class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        #3
        interfaces = (graphene.relay.Node, )


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)
