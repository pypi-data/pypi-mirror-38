__all__ = ["RdflibDjangoConfig"]

from django.apps import AppConfig
from django.db.models.signals import post_save

extra_namespaces = [
    {
        "prefix": "xml",
        "fixed": True,
        "uri": "http://www.w3.org/XML/1998/namespace"
    }
]


def UpdateNamespaces(sender, instance, created, **kwargs):
    if not created:
        return
    from .models import NamespaceModel
    from django.db.models import Q
    from rdflib import namespace
    for val in extra_namespaces:
        val2 = val.copy()
        fixed = val2.pop("fixed", False)
        store = instance
        if fixed:
            store = None
        if not NamespaceModel.objects.filter(
            Q(uri=val2["uri"]) | Q(prefix=val2["prefix"]),
            store=store
        ):
            NamespaceModel.objects.create(
                store=store,
                **val2
            )
        if not store:
            # cleanup old namespaces
            NamespaceModel.objects.filter(
                Q(uri=val["uri"]) | Q(prefix=val["prefix"])
            ).exclude(store__isnull=True).delete()
    for key in namespace.__all__:
        val = getattr(namespace, key)
        if isinstance(val, namespace.Namespace):
            if not NamespaceModel.objects.filter(
                Q(uri=val.uri) | Q(prefix=key.lower()),
                store=instance
            ):
                NamespaceModel.objects.create(
                    prefix=key.lower(),
                    uri=val.uri,
                    store=instance
                )
        elif isinstance(val, namespace.ClosedNamespace):
            if not NamespaceModel.objects.filter(
                Q(uri=val.uri) | Q(prefix=key.lower()),
                store=None
            ):
                NamespaceModel.objects.create(
                    prefix=key.lower(),
                    uri=val.uri,
                    store=None
                )
            # cleanup old namespaces
            NamespaceModel.objects.filter(
                Q(uri=val.uri) | Q(prefix=key.lower())
            ).exclude(store__isnull=True).delete()


class RdflibDjangoConfig(AppConfig):
    name = "rdflib_django"

    def ready(self):
        from .models import Store
        post_save.connect(
            UpdateNamespaces, sender=Store
        )
