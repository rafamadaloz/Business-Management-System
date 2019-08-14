# -*- coding: utf-8 -*-
from django.contrib import messages
from django.urls import reverse_lazy

from SGEO.apps.base.custom_views import CustomCreateView, CustomUpdateView, CustomTemplateView, CustomListView

from SGEO.apps.plano.models import Plano, UsuariosAdicionais, NotasAdicionais, BoletosAdicionais, Pagamento, TipoPlano
from SGEO.apps.cadastro.models import MinhaEmpresa
from SGEO.apps.login.models import Usuario
from SGEO.apps.plano.forms import PlanoForm
import requests
import json
from datetime import datetime
from dicttoxml import dicttoxml
import xmltodict


class MeuPlanoView(CustomListView):
    template_name = 'plano/meu_plano.html'
    model = Pagamento
    context_object_name = 'all_pagamentos'
    permission_codename = 'view_meu_plano'

    def get_context_data(self, **kwargs):
        context = super(MeuPlanoView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'MEU PLANO'
        context['add_plano'] = reverse_lazy('plano:adicionarplanoview')
        return context


class AdicionarPlanoView(CustomTemplateView):
    form_class = PlanoForm
    template_name = "plano/adicionar_plano.html"
    success_url = reverse_lazy('plano:adicionarplanoview')
    success_message = "Plano <b>%(descricao)s </b>atualizado com sucesso."
    permission_codename = 'add_plano'
    id_pagseguro = False

    def get_context_data(self, **kwargs):
        context = super(AdicionarPlanoView, self).get_context_data(**kwargs)
        context['all_boletos_adicionais'] = BoletosAdicionais.objects.all()
        context['all_notas_adicionais'] = NotasAdicionais.objects.all()
        context['all_usuarios_adicionais'] = UsuariosAdicionais.objects.all()
        context['all_tipos_plano'] = TipoPlano.objects.all()
        if self.id_pagseguro:
            context['id_pagseguro'] = self.id_pagseguro
        return context

    def get_object(self):
        try:
            conf_nfe = Plano.objects.all()[:1].get()
        except Plano.DoesNotExist:
            conf_nfe = None

        return conf_nfe

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PlanoForm(prefix='plano_form', instance=self.object)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PlanoForm(request.POST, prefix='plano_form', instance=self.object)

        if form.is_valid():

            self.object = form.save(commit=False)

            self.object.data_inicio = datetime.now().date()
            tipo_pagamento = ''

            if self.object.tipo_pagamento == '0':
                valor_plano = self.object.tipo_plano.valor_mensal
                tipo_pagamento = ' Mensal'
            elif self.object.tipo_pagamento == '1':
                valor_plano = self.object.tipo_plano.valor_anual
                tipo_pagamento = ' Anual'

            if self.object.notas_adicionais:
                valor_notas_adicionais = self.object.notas_adicionais.valor
            else:
                valor_notas_adicionais = 0
            if self.object.boletos_adicionais:
                valor_boletos_adicionais = self.object.boletos_adicionais.valor
            else:
                valor_boletos_adicionais = 0
            if self.object.usuarios_adicionais:
                valor_usuarios_adicionais = self.object.usuarios_adicionais.valor
            else:
                valor_usuarios_adicionais = 0

            self.object.valor = valor_plano + valor_boletos_adicionais + valor_notas_adicionais + valor_usuarios_adicionais

            self.object.save()


            token = '2CBD7E400E1D4B9F9B51CCE30B02E8B7'
            # token = "2b6eb7dc-2f5a-4cc2-aafe-73df9940b0fd0fc14a07486d969db98effc37aa09792aeca-eb09-43cf-9d17-ba6bfe06eb73"

            email = 'financeiro@SGEOerp.com.br'

            url = "https://ws.sandbox.pagseguro.uol.com.br/v2/checkout"
            # url = "https://ws.pagseguro.uol.com.br/v2/checkout"

            url = url + "?email=" + email + "&token=" + token

            params = {}

            params['shippingAddressRequired'] = 'false',

            # url = "https://ws.sandbox.pagseguro.uol.com.br/v2/checkout?email=financeiro@SGEOerp.com.br&token=2CBD7E400E1D4B9F9B51CCE30B02E8B7"

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            params['currency'] = 'BRL'
            params['itemId1'] = self.object.id
            params['itemDescription1'] = 'Plano ' + self.object.tipo_plano.nome + tipo_pagamento
            params['itemAmount1'] = valor_plano
            params['itemQuantity1'] = 1
            params['itemWeight1'] = 0

            id = 2

            if self.object.notas_adicionais:
                params['itemId' + str(id)] = 10 + self.object.notas_adicionais.id
                params['itemDescription' + str(id)] = 'Notas Adicionais +' + str(self.object.notas_adicionais.quantidade)
                params['itemAmount' + str(id)] = self.object.notas_adicionais.valor
                params['itemQuantity' + str(id)] = 1
                params['itemWeight' + str(id)] = 0
                id += 1

            if self.object.boletos_adicionais:
                params['itemId' + str(id)] = 20 + self.object.boletos_adicionais.id
                params['itemDescription' + str(id)] = 'Boletos Adicionais +' + str(self.object.boletos_adicionais.quantidade)
                params['itemAmount' + str(id)] = self.object.boletos_adicionais.valor
                params['itemQuantity' + str(id)] = 1
                params['itemWeight' + str(id)] = 0
                id += 1

            if self.object.usuarios_adicionais:
                params['itemId' + str(id)] = 30 + self.object.usuarios_adicionais.id
                params['itemDescription' + str(id)] = 'Usuários Adicionais +' + str(self.object.usuarios_adicionais.quantidade)
                params['itemAmount' + str(id)] = self.object.usuarios_adicionais.valor
                params['itemQuantity' + str(id)] = 1
                params['itemWeight' + str(id)] = 0
                id += 1

            user = request.user.id
            if user:
                usuario = Usuario.objects.get(user_id=user)
                m_empresa = MinhaEmpresa.objects.get(
                    m_usuario=usuario).m_empresa
                if m_empresa:
                    email = m_empresa.email_padrao.email
                    telefone = m_empresa.telefone_padrao.get_telefone_apenas_digitos()
                    nome = m_empresa.nome_razao_social
                    if nome:
                        params['senderName'] = nome
                    if email:
                        params['senderEmail'] = email
                    if telefone:
                        params['senderAreaCode'] = telefone[:2]
                        params['senderPhone'] = telefone[2:]
                    if m_empresa.tipo_pessoa == 'PJ':
                        if m_empresa.cpf_cnpj_apenas_digitos:
                            params['senderCNPJ'] = m_empresa.cpf_cnpj_apenas_digitos

                    elif m_empresa.tipo_pessoa == 'PF':
                        if m_empresa.cpf_cnpj_apenas_digitos:
                            params['senderCPF'] = m_empresa.cpf_cnpj_apenas_digitos

            r = requests.post(url, headers=headers, params=params)
            resposta = xmltodict.parse(r.text)

            if r.status_code is 200:
                self.id_pagseguro = resposta['checkout']['code']
                Pagamento.objects.create(
                    data_criacao=datetime.now().date(),
                    valor=self.object.valor
                )
                messages.success(request, "Por favor, aguarde o processamento do pagamento.")
            else:
                messages.error(request, str(r.text))


            return self.form_valid(form)

        return self.form_invalid(form=form)
