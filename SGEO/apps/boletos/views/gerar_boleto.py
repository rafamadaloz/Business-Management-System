# -*- coding: utf-8 -*-
import requests

from requests.auth import HTTPBasicAuth
from django.http import FileResponse
from django.http import FileResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from decimal import Decimal
from datetime import datetime

from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView, \
    CustomTemplateView

from SGEO.apps.boletos.forms import BoletoForm, ConfiguracoesBoletoForm
from SGEO.apps.boletos.models import Boleto, ConfiguracaoBoleto


class AdicionarBoletoAvulsoView(CustomCreateView):
    template_name = "boletos/boletos/boletos_add.html"
    form_class = BoletoForm
    model = Boleto
    success_url = reverse_lazy('boletos:listaboletosview')
    success_message = "Boleto N°<b>%(numero)s </b>gerada com sucesso."
    permission_codename = 'add_boleto'

    def get_context_data(self, **kwargs):
        context = super(AdicionarBoletoAvulsoView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR NOVO BOLETO'
        context['return_url'] = reverse_lazy('boletos:listaboletosview')
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form = BoletoForm()
        # form.initial['status'] = 1
        form.initial['documento'] = 'documento teste'
        form.initial['emissao'] = datetime.today().strftime('%d/%m/%Y')

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None

        configuracao = ConfiguracaoBoleto.objects.last()

        data = {

            'boleto.emissao': request.POST['emissao'],
            'boleto.vencimento': request.POST['vencimento'],
            'boleto.documento': request.POST['documento'],
            'boleto.numero': request.POST['numero'],
            'boleto.titulo': request.POST['titulo'],
            'boleto.valor': request.POST['valor'],
            'boleto.conta.banco': configuracao.banco,
            'boleto.conta.agencia': configuracao.agencia,
            'boleto.conta.numero': configuracao.numero + configuracao.digito,
            'boleto.conta.carteira': configuracao.carteira,
            'boleto.beneficiario.nome': configuracao.nome_razao_social,
            'boleto.beneficiario.cprf': configuracao.cpf_cnpj,
            'boleto.beneficiario.endereco.cep': configuracao.cep,
            'boleto.beneficiario.endereco.uf': configuracao.estado,
            'boleto.beneficiario.endereco.localidade': configuracao.cidade,
            'boleto.beneficiario.endereco.bairro': configuracao.bairro,
            'boleto.beneficiario.endereco.logradouro': configuracao.logradouro,
            'boleto.beneficiario.endereco.numero': configuracao.numero,
            'boleto.beneficiario.endereco.complemento': configuracao.complemento,
            'boleto.pagador.nome': 'Nome pagador teste',
            'boleto.pagador.cpfr': '111.111.111.-11',
            'boleto.pagador.endereco.cep': '36240-000',
            'boleto.pagador.endereco.uf': 'MG',
            'boleto.pagador.endereco.localidade': 'Santos Dumont',
            'boleto.pagador.endereco.bairro': 'Casa Natal',
            'boleto.pagador.endereco.logradouro': 'BR-499',
            'boleto.pagador.endereco.numero': 's/n',
            'boleto.pagador.endereco.complemento': 'Sítio - Subindo a serra da Mantiqueira',
            'boleto.instrucao': ['instrucao teste'],
        }

        r = requests.post("https://sandbox.boletocloud.com", data)
        messages.error(request, r.content)

        # req_post = request.POST.copy()
        # req_post['valor'] = req_post['valor'].replace('.', '')
        # request.POST = req_post

        form = BoletoForm(request.POST)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form)


class BoletosListView(CustomListView):
    model = Boleto
    template_name = 'boletos/boletos/boletos_list.html'
    context_object_name = 'all_boletos'
    success_url = reverse_lazy('boletos:listaboletosview')
    permission_codename = 'view_boleto'


class EditarBoletoBaseView(CustomUpdateView):

    def get_context_data(self, **kwargs):
        context = super(EditarBoletoBaseView, self).get_context_data(**kwargs)
        context['edit_nfe'] = True
        return self.view_context(context)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, n_nf=self.object.id)


# class AdicionarCentroCustoView(CustomCreateView):
#     template_name = "base/popup_form.html"
#     form_class = CentroCustoForm
#     model = CentroCusto
#     success_url = reverse_lazy('financeiro:addcentrocustoview')
#     permission_codename = 'add_centrocusto'
#
#     def get_context_data(self, **kwargs):
#         context = super(AdicionarCentroCustoView,
#                         self).get_context_data(**kwargs)
#         context['titulo'] = 'Adicionar Centro de Custo'
#         return context


class EditarBoletoAvulsoView(CustomUpdateView):
    template_name = "boletos/boletos/boletos_edit.html"
    form_class = BoletoForm
    model = Boleto
    success_url = reverse_lazy('boletos:listaboletosview')
    permission_codename = 'change_boleto'

    def get_context_data(self, **kwargs):
        context = super(EditarBoletoAvulsoView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Editar Boleto: {0}'.format(str(self.object))
        return context

    def post(self, request, *args, **kwargs):

        configuracao = ConfiguracaoBoleto.objects.last()

        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

        auth = HTTPBasicAuth('api-key_9zDxNVlGxOSFfYCbibLYHdmyQ7BMvW0nl-bxZd-cEl4=', 'token')

        data = {

            'boleto.emissao': datetime.strptime(request.POST['emissao'], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'boleto.vencimento': datetime.strptime(request.POST['vencimento'], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'boleto.documento': request.POST['documento'],
            'boleto.numero': request.POST['numero'],
            'boleto.titulo': request.POST['titulo'],
            'boleto.valor': request.POST['valor'],
            'boleto.conta.banco': configuracao.banco,
            'boleto.conta.agencia': configuracao.agencia,
            'boleto.conta.numero': configuracao.numero + configuracao.digito,
            'boleto.conta.carteira': '1',
            'boleto.conta.convenio': '242-4',
            'boleto.beneficiario.nome': configuracao.nome_razao_social,
            'boleto.beneficiario.cprf': '612.335.280-68',
            'boleto.beneficiario.endereco.cep': configuracao.cep,
            'boleto.beneficiario.endereco.uf': configuracao.estado,
            'boleto.beneficiario.endereco.localidade': configuracao.cidade,
            'boleto.beneficiario.endereco.bairro': configuracao.bairro,
            'boleto.beneficiario.endereco.logradouro': configuracao.logradouro,
            'boleto.beneficiario.endereco.numero': configuracao.numero,
            'boleto.beneficiario.endereco.complemento': configuracao.complemento,
            'boleto.pagador.nome': 'Nome pagador teste',
            'boleto.pagador.cprf': '111.111.111-11',
            'boleto.pagador.endereco.cep': '36240-000',
            'boleto.pagador.endereco.uf': 'MG',
            'boleto.pagador.endereco.localidade': 'Santos Dumont',
            'boleto.pagador.endereco.bairro': 'Casa Natal',
            'boleto.pagador.endereco.logradouro': 'BR-499',
            'boleto.pagador.endereco.numero': 's/n',
            'boleto.pagador.endereco.complemento': 'Sítio - Subindo a serra da Mantiqueira',
            'boleto.instrucao': ['instrucao teste'],
        }

        # req_post = request.POST.copy()
        # req_post['valor'] = req_post['valor'].replace('.', '')
        # request.POST = req_post

        self.object = self.get_object()
        form_class = self.get_form_class()

        form = form_class(request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            ticket = requests.post("https://sandbox.boletocloud.com/api/v1/boletos", auth=auth, data=data,
                                   headers=headers)

            if ticket.status_code is 201:
                messages.success(request, 'Boleto gerado com sucesso')
                self.object.status = '1'
                self.object.token = ticket.headers['X-BoletoCloud-Token']
            else:
                messages.error(request, ticket.content)

            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form)


class GerarPDFBoleto(CustomView):

    def get(self, request, *args, **kwargs):

        boleto_id = kwargs.get('pk', None)

        if not boleto_id:
            return HttpResponse('Objeto não encontrado.')

        obj = Boleto.objects.get(pk=boleto_id)

        headers = {'content-type': 'application/pdf'}

        url = "https://sandbox.boletocloud.com/api/v1/boletos/" + obj.token

        auth = HTTPBasicAuth('api-key_9zDxNVlGxOSFfYCbibLYHdmyQ7BMvW0nl-bxZd-cEl4=', 'token')

        ticket = requests.get(url, auth=auth, headers=headers)

        # return HttpResponse(ticket.status_code)

        nome_arquivo = 'Boleto_' + str(obj.numero) + '.pdf'


        if ticket.status_code is 200:
            resp = HttpResponse(content_type='application/pdf')
            resp['Content-Disposition'] = 'filename="' + nome_arquivo + '"'
            resp.write(ticket.content)
            return resp
        else:
            return messages.error(request, ticket.content)
