# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from dal import autocomplete
from decimal import Decimal
from datetime import datetime
from django.shortcuts import redirect, render
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from SGEO.apps.cadastro.models import MinhaEmpresa
from SGEO.apps.login.models import Usuario
from SGEO.apps.cadastro.models import Produto
from SGEO.apps.pdv.forms import AddToCartForm
from SGEO.apps.pdv.models import ItensVendaPdv, VendaPdv


class AutoCompleteView(FormView):
    def get(self, request, *args, **kwargs):

        try:

            products = Produto.objects.filter(
                descricao__contains=request.GET.get('product'),
                codigo_barras__contains=request.GET.get('product')
            )

            product_list = []

            for item in products:
                product_list.append({
                    'descricao': item.descricao,
                    "codigo_barras": item.codigo_barras,
                    "codigo": item.codigo,
                    "valor_unit": str(item.venda),
                    "produto_id": str(item.id),
                })

            response = json.dumps(product_list)

        except ObjectDoesNotExist as exp:

            err_str = str(exp) + str(" or not active")

            response = json.dumps({'err': err_str})

        return HttpResponse(response, content_type="text/json")


class PDVView(TemplateView):
    template_name = 'pdv/pdv.html'

    def get_context_data(self, **kwargs):
        context = super(PDVView, self).get_context_data(**kwargs)

        context['usuario'] = self.request.user.username

        try:
            user_empresa = MinhaEmpresa.objects.get(
                m_usuario=Usuario.objects.get(user=self.request.user)).m_empresa
            if user_empresa:
                context['user_empresa'] = user_empresa
        except:
            pass

        return context

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():
            data = request.session['cart_products']
        else:
            data = None

        return render(request, self.template_name, {'cart_products': data})


class AddToCart(FormView):
    raise_exception = True
    form_class = AddToCartForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            descricao = form.cleaned_data['descricao']
            codigo = form.cleaned_data['codigo']
            quantidade = form.cleaned_data['quantidade']
            valor_unit = form.cleaned_data['valor_unit']
            produto_id = form.cleaned_data['produto_id']
            valor_total = form.cleaned_data['valor_total']

            new_product = {
                'descricao': descricao,
                'produto_id': produto_id,
                'valor_unit': valor_unit,
                'valor_total': valor_total,
                'quantidade': quantidade,
                'codigo': codigo,
            }

            if 'cart_products' not in request.session.keys():  # add first product to cart_products list

                cart_products = list()

                cart_products.append(new_product)

                request.session['cart_products'] = cart_products

            else:

                cart_products = request.session['cart_products']
                product_ids = [pk['produto_id'] for pk in cart_products]

                if new_product['produto_id'] not in product_ids:

                    cart_products.append(new_product)
                else:

                    for product in cart_products:

                        quantity = product['quantidade'] + new_product['quantidade']
                        valor_total = quantity * new_product['valor_unit']

                        if product['produto_id'] == new_product['produto_id']:
                            product['quantidade'] = quantity
                            product['valor_unit'] = new_product['valor_unit']
                            product['valor_total'] = valor_total

                request.session['cart_products'] = cart_products

        else:
            cart_products = {"error": form.errors}

        return HttpResponse(
            json.dumps(cart_products),
            content_type="text/json"
        )


class DeleterCartProduct(TemplateView):
    raise_exception = True

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():

            if self.kwargs['produto_id'] in [p['produto_id'] for p in request.session['cart_products']]:

                cart_products = request.session['cart_products']

                for product in cart_products:

                    if product['produto_id'] == self.kwargs['produto_id']:

                        cart_products.remove(product)

                        request.session['cart_products'] = cart_products

        return redirect(to='/pdv/pdv')


class ClearCart(TemplateView):

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():

            del request.session['cart_products']
        else:
            pass

        return redirect(to='/pdv/pdv')


class CheckOut(FormView):
    raise_exception = True

    def get(self, request, *args, **kwargs):

        venda = VendaPdv(
            data_emissao=datetime.now(),
            valor_total=0.00,
            status='1',
            vendedor=request.user.username
        )

        venda.save()

        for product in request.session['cart_products']:

            product_obj = Produto.objects.get(pk=product['produto_id'])

            itens_venda = ItensVendaPdv(
                produto=product_obj,
                venda_pdv_id=venda,
                quantidade=product['quantidade'],
                valor_unit=product['valor_unit'],
                subtotal=float(product['quantidade'])*float(product['valor_unit'])
            )

            itens_venda.save()
            venda.valor_total += itens_venda.subtotal
            venda.save()

        del request.session['cart_products']

        return redirect(to='/pdv/pdv/')


class SaleView(TemplateView):
    template_name = 'pdv/test.html'

    def get_context_data(self, **kwargs):
        context = super(SaleView, self).get_context_data(**kwargs)
        return context






