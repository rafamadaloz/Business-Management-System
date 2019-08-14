from dal import autocomplete
from SGEO.apps.cadastro.models import Produto
from SGEO.apps.pdv.models import ProdutoPDV
from django import forms


class PDVForm(forms.ModelForm):
    class Meta:
        model = ProdutoPDV
        fields = ('__all__')
        widgets = {
            'produto': autocomplete.ModelSelect2(url='pdv:search-products')
        }


class AddToCartForm(forms.Form):

    descricao = forms.CharField(max_length=150)
    valor_unit = forms.FloatField(initial=0.0)
    quantidade = forms.CharField(max_length=150)
    valor_total = forms.FloatField(initial=0.0)
    produto_id = forms.IntegerField()
    codigo = forms.CharField(max_length=150)
