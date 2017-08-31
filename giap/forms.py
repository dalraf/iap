from django.forms import modelform_factory, modelform_factory, modelformset_factory
from giap.models import cliente, cooperativa, central, pa



formaddcliente = modelform_factory(cliente,
    fields=("pa", "tipodepessoa", "numcpfcpnj", "nome_cliente"),
    )

formaddcentral = modelform_factory(central,
    fields=("sigla_central", "numcentral",),
    )

formsetcentral = modelformset_factory(central,
    fields=("sigla_central", "numcentral",),
    can_delete=True,
    )


formaddcooperativa = modelform_factory(cooperativa,
    fields=("sigla_cooperativa", "numcooperativa","central"),
    )

formsetcooperativa = modelformset_factory(cooperativa,
    fields=("sigla_cooperativa", "numcooperativa","central"),
    )

formaddpa = modelform_factory(pa,
    fields=("sigla_pa", "numpa", "cooperativa"),
    )

formsetpa = modelformset_factory(pa,
    fields=("sigla_pa", "numpa", "cooperativa"),
    )

