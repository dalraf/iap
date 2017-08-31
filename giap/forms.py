from django.forms import modelform_factory, modelformset_factory
from giap.models import cliente, cooperativa, central, pa


formaddcliente = modelform_factory(cliente,
    fields=("pa", "tipodepessoa", "numcpfcpnj", "nome_cliente"),
    )

formaddcentral = modelformset_factory(central,
    fields=("sigla_central", "numcentral",),
    )

formaddcooperativa = modelformset_factory(cooperativa,
    fields=("sigla_cooperativa", "numcooperativa","central"),
    )

formaddpa = modelformset_factory(pa,
    fields=("sigla_pa", "numpa", "cooperativa"),
    )
