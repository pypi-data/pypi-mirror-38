import collections

import django.apps
from django.db.models.fields.related import ForeignKey

from . import attr, auto_repr, first, memorize


@memorize
def get_all_model_relations():
    class Relation:
        def __init__(self, model, attribute, verbose_name):
            self.attribute = attribute
            self.model = model
            self.verbose_name = verbose_name

    models = django.apps.apps.get_models()

    def init_model_relations():
        for model in models:
            fields = attr(model, '_meta.fields')
            for field in fields:
                remote_field = attr(field, "remote_field")
                if remote_field:
                    related_model = attr(remote_field, "model")
                    field = attr(remote_field, "field")
                    if type(field) is ForeignKey:
                        relations = attr(model, "relations", [])
                        relations.append(Relation(related_model, attr(field, "name"), attr(field, "verbose_name")))
                        setattr(model, "relations", relations)

    init_model_relations()

    def _get_attributes(model, name=None):
        relations = attr(model, "relations", [])
        names = []
        for relation in relations:
            new_name = f"{name}.{relation.attribute}" if name else relation.attribute
            new_names = _get_attributes(relation.model, new_name)
            if new_names:
                names += new_names
            else:
                names.append(new_name)

        return names

    def get_field_relation_model(model, attribute):
        _cls = model
        for name in attribute.split("."):
            field = attr(_cls, f"{name}.field")
            _cls = attr(field, f"remote_field.model")
        return _cls

    def _get_all(model):
        _result = []
        attributes = _get_attributes(model)
        if attributes:
            for attribute in attributes:
                names = attribute.split(".")
                for i in range(1, len(names) + 1):
                    sub_attribute = ".".join(names[0:i])
                    cls = get_field_relation_model(model, sub_attribute)
                    _result.append((sub_attribute, cls))
        return _result

    result = collections.OrderedDict()
    for model in models:
        relations = _get_all(model)
        groups, group = [], []
        last_attribute = None
        for relation in relations:
            if not group or relation[0].startswith(last_attribute):
                group.append(relation)
            elif group:
                groups.append(group)
                group = [relation]
            last_attribute = relation[0]
        if group:
            groups.append(group)
        result[model] = groups

    return result


def get_relation_group(model):
    return get_all_model_relations().get(model)


@memorize
def get_model_fields(cls) -> list:
    return attr(cls, '_meta.fields')


@memorize
def get_model_fields_without_relation(model):
    fields = model._meta.fields
    result = []
    for field in fields:
        name = field.name
        if 'ForeignKey' in str(field.__class__):
            name = "%s|%s_id" % (name, name)
        result.append(name)
    return result


@memorize
def get_many_to_many_fields(cls) -> list:
    return attr(cls, '_meta.many_to_many')


def get_model_field(cls, name):
    return first([f for f in attr(cls, '_meta.fields') if f.name == name])


@memorize
def get_model_field_names(cls) -> list:
    return [x.name for x in get_model_fields(cls)]


@memorize
def get_ancestor_attribute(child_cls, parent_cls, property_name=""):
    for name, x in get_parents(child_cls):
        name = name if not property_name else property_name + "." + name
        if x is child_cls or x is parent_cls:
            return name

        return get_ancestor_attribute(x, parent_cls, name)


@memorize
def get_ancestors(cls, max_cls=None):
    result = []
    if max_cls and not get_ancestor_attribute(cls, max_cls): return result
    if cls is not max_cls:
        foreign_fields = get_parents(cls)
        if foreign_fields:
            name, foreign_cls = foreign_fields[0]

            result.append((name, foreign_cls))
            if foreign_cls is not max_cls and foreign_cls is not cls:
                result += get_ancestors(foreign_cls, max_cls)
    return result


@memorize
def get_ancestors_names(cls, max_cls=None):
    return [name for (name, _) in get_ancestors(cls, max_cls)]


@memorize
def get_parents(cls) -> list:
    result = []
    for field in get_model_fields(cls):
        related_fields = attr(field, '_related_fields')
        if related_fields and isinstance(related_fields, list):
            item = related_fields[0]
            if isinstance(item, tuple):
                (i, _) = item
                if isinstance(i, ForeignKey):
                    result.append((field.name, i.related_model))
    return result


@auto_repr
class Field:
    def __init__(self, name, verbose, attribute_name, class_name=None, orderable=True, is_image=False):
        self.name = name
        self.verbose = verbose
        self.attribute_name = attribute_name
        self.class_name = class_name
        self.orderable = orderable
        self.is_image = is_image

# @memorize
