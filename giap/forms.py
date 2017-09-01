from django.forms import modelform_factory, modelform_factory, modelformset_factory
from giap.models import cliente, cooperativa, central, pa


formcentral = modelform_factory(central,
    fields=("sigla_central", "numcentral",),
    )
