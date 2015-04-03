from django.contrib.admin import site as admin_site
from .admin import CreatedUpdatedBy, NameSlug, LocalPreview, AutoGroupMeta


class site(object):

    @staticmethod
    def add_base(admin_class, base):
        if base not in admin_class.__bases__:
            admin_class.__bases__ = (base,) + admin_class.__bases__

    @staticmethod
    def register(model, admin_class):
        def _list_has_all_values(superset, subset):
            return all(map(lambda value: value in superset, subset))

        field_names = map(lambda field: field.name, model._meta.fields)

        if _list_has_all_values(field_names, ('created_by', 'updated_by')):
            site.add_base(admin_class, CreatedUpdatedBy)

        if _list_has_all_values(field_names, ('name', 'slug')):
            site.add_base(admin_class, NameSlug)

        if 'is_active' in field_names:
            site.add_base(admin_class, LocalPreview)

        site.add_base(admin_class, AutoGroupMeta)

        admin_site.register(model, admin_class)
