import graphene


class Error(graphene.ObjectType):
    field = graphene.String(required=False)
    message = graphene.String()
    code = graphene.String()
