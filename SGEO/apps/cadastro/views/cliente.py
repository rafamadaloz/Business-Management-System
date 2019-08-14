# -*- coding: utf-8 -*-
import csv
import io
from datetime import datetime
from django.urls import reverse_lazy
from SGEO.apps.base.custom_views import CustomView
from django.shortcuts import redirect
from django.contrib import messages

from SGEO.apps.cadastro.forms import ClienteForm
from SGEO.apps.cadastro.models import Cliente, Pessoa, PessoaFisica, PessoaJuridica, Endereco, Email, Telefone, Banco, Site

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarClienteView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listaclientesview')
    success_message = "Cliente <b>%(nome_razao_social)s </b>adicionado com sucesso."
    permission_codename = 'add_cliente'

    def get_context_data(self, **kwargs):
        context = super(AdicionarClienteView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR CLIENTE'
        context['return_url'] = reverse_lazy('cadastro:listaclientesview')
        context['tipo_pessoa'] = 'cliente'
        return context

    def get(self, request, *args, **kwargs):
        form = ClienteForm(prefix='cliente_form')
        return super(AdicionarClienteView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        req_post['cliente_form-limite_de_credito'] = req_post['cliente_form-limite_de_credito'].replace(
            '.', '')
        # req_post['cliente_form-limite_restante'] = req_post['cliente_form-limite_restante'].replace(
        #     '.', '')
        req_post['cliente_form-comissao_vendedor'] = req_post['cliente_form-comissao_vendedor'].replace(
            '.', '')
        request.POST = req_post
        form = ClienteForm(request.POST, request.FILES,
                           prefix='cliente_form', request=request)
        return super(AdicionarClienteView, self).post(request, form, *args, **kwargs)


class ClientesListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Cliente
    context_object_name = 'all_clientes'
    success_url = reverse_lazy('cadastro:listaclientesview')
    permission_codename = 'view_cliente'

    def get_context_data(self, **kwargs):
        context = super(ClientesListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CLIENTES CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addclienteview')
        context['tipo_pessoa'] = 'cliente'
        context['importar_cliente_url'] = reverse_lazy(
            'cadastro:importarclienteview')
        return context


class ImportarClienteView(AdicionarPessoaView):
    permission_codename = ['add_cliente', 'change_cliente', 'view_cliente']

    def get_redirect_url(self):
        return redirect(reverse_lazy('cadastro:listaclientesview'))

    def post(self, request, *args, **kwargs):
        if len(request.FILES):
            try:
                self.importar_csv(request)
            except Exception as e:
                messages.error(
                    request, 'O seguinte erro foi encontrado ao tentar importar o arquivo CSV: ' + str(e))
        else:
            messages.error(request, 'Arquivo CSV não selecionado.')
        return self.get_redirect_url()

    def importar_csv(self, request):

        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return messages.error(request, "O arquivo não tem a extensão .csv!")

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        colunas_csv = csv.reader(io_string, delimiter=';', quotechar="|")
        qtd_colunas = 0
        dados = {}
        for column in colunas_csv:

            if column[12] == '':
                column[12] = float('0.00')
            else:
                column[12] = float(column[12].replace(".", "").replace(",", "."))
                messages.success(request, column[12])

            if column[13] == '0':
                column[13] = False
            else:
                column[13] = True

            try:

                cliente_obj, created = Cliente.objects.get_or_create(
                    nome_razao_social=column[0],
                    tipo_pessoa=str(column[1]),
                    criado_por=request.user,
                    inscricao_municipal=column[4],
                    indicador_ie=column[10],
                    id_estrangeiro=column[11],
                    limite_de_credito=column[12],
                    status_ativo=column[13],
                    informacoes_adicionais=column[14],
                )
            except Exception as e:
                messages.error(request, "Erro ao importar dados cliente: " + str(e))

            if column[1] == str('PF'):

                try:

                    pessoa_fisica_obj, created = PessoaFisica.objects.get_or_create(
                        pessoa_id=cliente_obj,
                        cpf=column[2],
                        rg=column[3],
                        sexo=column[8],
                    )

                    if column[9] != '':
                        column[9] = datetime.strptime(column[9], '%d/%m/%Y').date()
                        pessoa_fisica_obj.nascimento = column[9]

                except Exception as e:
                    messages.error(request, "Erro ao importar dados pessoa física: " + str(e))

            elif column[1] == str('PJ'):

                try:
                    pessoa_jur_obj, created = PessoaJuridica.objects.get_or_create(
                        pessoa_id=cliente_obj,
                        cnpj=column[2],
                        inscricao_estadual=column[3],
                        responsavel=column[5],
                        sit_fiscal=column[6],
                        suframa=column[7],
                    )
                except Exception as e:
                    messages.error(request, "Erro ao importar dados pessoa jurídica: " + str(e))

            try:

                endereco_obj, created = Endereco.objects.get_or_create(
                    logradouro=column[15],
                    numero=column[16],
                    bairro=column[17],
                    complemento=column[18],
                    uf=column[19],
                    cep=column[20],
                    pessoa_end=cliente_obj
                )
            except Exception as e:
                messages.error(request, "Erro ao importar dados endereço: " + str(e))

            try:
                telefone_obj, created = Telefone.objects.get_or_create(
                    telefone=column[21],
                    pessoa_tel=cliente_obj
                )
            except Exception as e:
                messages.error(request, "Erro ao importar dados telefone: " + str(e))

            try:
                email_obj, created = Email.objects.get_or_create(
                    email=column[22],
                    pessoa_email=cliente_obj
                )
            except Exception as e:
                messages.error(request, "Erro ao importar dados email: " + str(e))

            try:
                site_obj, created = Site.objects.get_or_create(
                    site=column[23],
                    pessoa_site=cliente_obj

                )
            except Exception as e:
                messages.error(request, "Erro ao importar dados site: " + str(e))

            try:
                banco_obj, created = Banco.objects.get_or_create(
                    banco=column[24],
                    agencia=column[25],
                    conta=column[26],
                    digito=column[27],
                    pessoa_banco=cliente_obj
                )
            except Exception as e:
                messages.error(request, "Erro ao importar dados banco: " + str(e))

            qtd_colunas += 1

        messages.success(request, str(qtd_colunas) + ' clientes cadastrados com sucesso')

        # form = ClienteForm(dados)
        # if form.is_valid():
        #     cliente = form.save(commit=False)
        #     cliente.save()
        #     messages.success(request, str(qtd_colunas) + " clientes cadastrados com sucesso!")
        # else:
        #     messages.error(request, 'Não foi possível importar, verifique os dados da tabela.' + str(form.errors))


class EditarClienteView(EditarPessoaView):
    form_class = ClienteForm
    model = Cliente
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listaclientesview')
    success_message = "Cliente <b>%(nome_razao_social)s </b>editado com sucesso."
    permission_codename = 'change_cliente'

    def get_context_data(self, **kwargs):
        context = super(EditarClienteView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listaclientesview')
        context['tipo_pessoa'] = 'cliente'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "cliente_form"
        form = self.get_form(form_class)

        return super(EditarClienteView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        req_post['cliente_form-limite_de_credito'] = req_post['cliente_form-limite_de_credito'].replace(
            '.', '')
        req_post['cliente_form-comissao_vendedor'] = req_post['cliente_form-comissao_vendedor'].replace(
            '.', '')
        request.POST = req_post
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES,
                          prefix='cliente_form', instance=self.object, request=request)
        return super(EditarClienteView, self).post(request, form, *args, **kwargs)

