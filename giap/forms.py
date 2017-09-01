from django.forms import modelform_factory, HiddenInput
from giap.models import cliente, cooperativa, central, pa


formcentral = modelform_factory(central,
    fields=("sigla_central", "numcentral", "id"),
    )
