from django.forms import modelform_factory
from giap.models import cliente


formaddcliente = modelform_factory(cliente,
    fields=("pa", "tipodepessoa", "numcpfcpnj", "nome_cliente"),
    )
