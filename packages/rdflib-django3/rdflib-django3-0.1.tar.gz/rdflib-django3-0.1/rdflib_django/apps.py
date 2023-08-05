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
        if not NamespaceModel.objects.filter(
            Q(uri=val["uri"]) | Q(prefix=val["prefix"]),
            store=instance
        ):
            NamespaceModel.objects.create(
                store=instance,
                **val
            )
    for key in namespace.__all__:
        val = getattr(namespace, key)
        if isinstance(val, namespace.Namespace):
            if not NamespaceModel.objects.filter(
                Q(uri=val.uri) | Q(prefix=key.lower()),
                store=instance
            ):
                NamespaceModel.objects.create(
                    fixed=False,
                    prefix=key.lower(),
                    uri=val.uri,
                    store=instance
                )
        elif isinstance(val, namespace.ClosedNamespace):
            if not NamespaceModel.objects.filter(
                Q(uri=val.uri) | Q(prefix=key.lower()),
                store=instance
            ):
                NamespaceModel.objects.create(
                    fixed=True,
                    prefix=key.lower(),
                    uri=val.uri,
                    store=instance
                )


class RdflibDjangoConfig(AppConfig):
    name = "rdflib_django"

    def ready(self):
        from .models import Store
        post_save.connect(
            UpdateNamespaces, sender=Store
        )
