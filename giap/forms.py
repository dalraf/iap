# -*- coding: utf-8 -*-
from django.forms import modelform_factory, HiddenInput, ModelChoiceField
from django import forms
from giap.models import cliente, cooperativa, central, pa, transacao, sisbrcsv
from django.forms.extras.widgets import SelectDateWidget


formcentral = modelform_factory(central,
                                fields=("sigla_central", "numcentral", "id"),
                                )

formcooperativa = modelform_factory(cooperativa,
                                    fields=("sigla_cooperativa",
                                            "numcooperativa", "central"),
                                    )

formpa = modelform_factory(pa,
                           fields=("sigla_pa", "numpa", "cooperativa"),
                           )

formcliente = modelform_factory(cliente,
                                fields=("nome_cliente", "numcpfcnpj",
                                        "tipodepessoa", "pa"),
                                )

formclientecorrecao = modelform_factory(cliente,
                                fields=("nome_cliente", "numcpfcnpj",
                                        "tipodepessoa", "pa"),
                                widgets={"numcpfcnpj": forms.HiddenInput()},
                                )                                

formtransacao = modelform_factory(transacao,
                                  fields=("cliente", "produto",
                                          "vencimento"),
                                  )

formtransacaocorrecao = modelform_factory(transacao,
                                  fields=("cliente", "produto",
                                          "vencimento"),
                                  widgets={"cliente": forms.HiddenInput(), "produto": forms.HiddenInput()},
                                  )


formsisbrcsv = modelform_factory(sisbrcsv,
                                  fields=("datareferencia", "sisbrcsvfile",
                                          ),
                                  )

class formprocessarsisbr(forms.Form):
    sisbrcsv = forms.ModelChoiceField(label='Data de referência',queryset=sisbrcsv.objects.all(),required=False,empty_label=None)


class pesquisa(forms.Form):
    filtro = forms.CharField(label='Filtrar', required=False, max_length=100)
