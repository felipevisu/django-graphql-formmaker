import graphene
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from graphene.types.mutation import MutationOptions

from .types import Error
from .utils import get_error_code_from_error, snake_to_camel_case


def validation_error_to_error_type(validation_error: ValidationError) -> list:
    err_list = []
    if hasattr(validation_error, "error_dict"):
        for field, field_errors in validation_error.error_dict.items():
            field = None if field == NON_FIELD_ERRORS else snake_to_camel_case(field)
            for err in field_errors:
                err_list.append(
                    (
                        Error(field=field, message=err.messages[0]),
                        get_error_code_from_error(err),
                        err.params,
                    )
                )
    else:
        for err in validation_error.error_list:
            err_list.append(
                (
                    Error(message=err.messages[0]),
                    get_error_code_from_error(err),
                    err.params,
                )
            )
    return err_list


def get_error_fields(error_type_class, error_type_field):
    return {error_type_field: graphene.Field(graphene.List(error_type_class))}


class BaseMutation(graphene.Mutation):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, error_type_class=None, **options):
        if not _meta:
            _meta = MutationOptions(cls)

        _meta.error_type_class = error_type_class or Error
        super().__init_subclass_with_meta__(_meta=_meta, **options)
        cls._meta.fields.update(get_error_fields(error_type_class or Error, "errors"))

    @classmethod
    def mutate(cls, root, info, **data):
        try:
            response = cls.perform_mutation(root, info, **data)
            if response and response.errors is None:
                response.errors = []
            return response
        except ValidationError as e:
            return cls.handle_errors(e)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass

    @classmethod
    def clean_input(cls, input):
        pass

    @classmethod
    def handle_errors(cls, error: ValidationError, **extra):
        errors = validation_error_to_error_type(error)
        return cls.handle_typed_errors(errors, **extra)

    @classmethod
    def handle_typed_errors(cls, errors: list, **extra):
        typed_errors = []
        error_class_fields = set(cls._meta.error_type_class._meta.fields.keys())
        for e, code, params in errors:
            error_instance = cls._meta.error_type_class(
                field=e.field, message=e.message, code=code
            )
            if params:
                error_fields_in_params = set(params.keys()) & error_class_fields
                for error_field in error_fields_in_params:
                    setattr(error_instance, error_field, params[error_field])
            typed_errors.append(error_instance)
        return cls(errors=typed_errors, **extra)
