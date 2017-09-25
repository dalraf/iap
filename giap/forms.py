from django.forms import modelform_factory, HiddenInput
from django import forms
from giap.models import cliente, cooperativa, central, pa, transacao
from django.forms.extras.widgets import SelectDateWidget


class pesquisa(forms.Form):
    filtro = forms.CharField(label='Filtrar', required=False, max_length=100)


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
    fields=("cliente", "produto", "grupo", "vencimento" ),
    )