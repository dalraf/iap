from django.forms import modelform_factory, HiddenInput
from giap.models import cliente, cooperativa, central, pa, transacao


formcentral = modelform_factory(central,
    fields=("sigla_central", "numcentral", "id"),
    )

formcooperativa =  modelform_factory(cooperativa,
    fields=("sigla_cooperativa", "numcooperativa", "central"),
    )

formpa =  modelform_factory(pa,
    fields=("sigla_pa", "numpa", "cooperativa"),
    )

formcliente =  modelform_factory(cliente,
    fields=("nome_cliente", "numcpfcpnj", "tipodepessoa", "pa"),
    )

formtransacao =  modelform_factory(transacao,
    fields=("cliente", "produto", "grupo" ),
    )