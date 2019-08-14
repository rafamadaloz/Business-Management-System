# -*- coding: utf-8 -*-

from ofxparse import OfxParser
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse

from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView

from SGEO.apps.financeiro.forms import ContaPagarForm, ContaReceberForm, SaidaForm, EntradaForm, ContaPagarPrestacaoForm, ContaReceberPrestacaoForm
from SGEO.apps.financeiro.models import Lancamento, Saida, Entrada, MovimentoCaixa, SaidaPrestacao, EntradaPrestacao
from SGEO.apps.vendas.models import PedidoVenda
from SGEO.apps.compras.models import PedidoCompra
from SGEO.apps.estoque.models import SaidaEstoque, ItensMovimento, ProdutoEstocado
from SGEO.apps.cadastro.models import Cliente

from itertools import chain
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MovimentoCaixaMixin(object):

    def adicionar_novo_movimento_caixa(self, lancamento, novo_movimento):
        if isinstance(lancamento, Entrada):
            novo_movimento.entradas = novo_movimento.entradas + lancamento.valor_liquido
            novo_movimento.saldo_final = novo_movimento.saldo_final + lancamento.valor_liquido
            novo_movimento.save()
            # Atualizar os saldos dos proximos movimentos
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=novo_movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial + lancamento.valor_liquido
                m.saldo_final = m.saldo_final + lancamento.valor_liquido
                m.save()

        elif isinstance(lancamento, Saida):
            novo_movimento.saidas = novo_movimento.saidas + lancamento.valor_liquido
            novo_movimento.saldo_final = novo_movimento.saldo_final - lancamento.valor_liquido
            novo_movimento.save()
            # Atualizar os saldos dos proximos movimentos
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=novo_movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial - lancamento.valor_liquido
                m.saldo_final = m.saldo_final - lancamento.valor_liquido
                m.save()

    def remover_valor_movimento_caixa(self, lancamento, movimento, valor):
        if isinstance(lancamento, Entrada):
            movimento.entradas = movimento.entradas - valor
            movimento.saldo_final = movimento.saldo_final - valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial - valor
                m.saldo_final = m.saldo_final - valor
                m.save()
        elif isinstance(lancamento, Saida):
            movimento.saidas = movimento.saidas - valor
            movimento.saldo_final = movimento.saldo_final + valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial + valor
                m.saldo_final = m.saldo_final + valor
                m.save()

    def adicionar_valor_movimento_caixa(self, lancamento, movimento, valor):
        if isinstance(lancamento, Entrada):
            movimento.entradas = movimento.entradas + valor
            movimento.saldo_final = movimento.saldo_final + valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial + valor
                m.saldo_final = m.saldo_final + valor
                m.save()
        elif isinstance(lancamento, Saida):
            movimento.saidas = movimento.saidas + valor
            movimento.saldo_final = movimento.saldo_final - valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial - valor
                m.saldo_final = m.saldo_final - valor
                m.save()

    def verificar_remocao_movimento(self, movimento):
        # Deletar Caso essa seja a unica transacao do movimento antigo
        if ((movimento.saldo_final == movimento.saldo_inicial) and (movimento.entradas == 0)):
            movimento.delete()

    def atualizar_saldos(self, movimento):
        try:
            ultimo_mvmt = MovimentoCaixa.objects.filter(
                data_movimento__lt=movimento.data_movimento).latest('data_movimento')
            movimento.saldo_inicial = ultimo_mvmt.saldo_final
            movimento.saldo_final = movimento.saldo_inicial
            movimento.save()
        except MovimentoCaixa.DoesNotExist:
            pass


class AdicionarLancamentoBaseView(CustomCreateView, MovimentoCaixaMixin):
    permission_codename = 'add_lancamento'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = form_class(user=request.user)
        form.initial['data_pagamento'] = datetime.today().strftime('%d/%m/%Y')
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                'juros' in key or
                    'abatimento' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = form_class(request.POST, user=request.user)

        if form.is_valid():
            self.object = form.save(commit=False)

            if self.object.movimentar_caixa:
                mvmt = None
                created = None
                if self.object.data_pagamento:
                    mvmt, created = MovimentoCaixa.objects.get_or_create(
                        data_movimento=self.object.data_pagamento)
                elif self.object.data_vencimento:
                    mvmt, created = MovimentoCaixa.objects.get_or_create(
                        data_movimento=self.object.data_vencimento)

                if mvmt:
                    if created:
                        self.atualizar_saldos(mvmt)

                    self.adicionar_novo_movimento_caixa(
                        lancamento=self.object, novo_movimento=mvmt)
                    mvmt.save()
                    self.object.movimento_caixa = mvmt

            self.object.save()
            return self.form_valid(form)

        return self.form_invalid(form)


class ImportarLancamentoView(AdicionarLancamentoBaseView):
    permission_codename = ['add_lancamento', 'change_lancamento', 'view_lancamento']

    def get_redirect_url(self):
        return redirect(reverse_lazy('financeiro:listalancamentoview'))

    def post(self, request, *args, **kwargs):
        if len(request.FILES):
            try:
                self.importar_ofx(request)
            except Exception as e:
                messages.error(
                    request, 'O seguinte erro foi encontrado ao tentar importar o arquivo OFX: ' + str(e))
        else:
            messages.error(request, 'Arquivo OFX não selecionado.')
        return self.get_redirect_url()

    def importar_ofx(self, request):

        ofx_file = request.FILES['file']

        ofx = OfxParser.parse(ofx_file)

        account = ofx.account

        statement = account.statement

        qtd = 0

        for transaction in statement.transactions:

            data = transaction.date
            numero = transaction.checknum
            descricao = str(transaction.memo) + " Nº " + str(numero)
            valor = transaction.amount

            if valor < 0:
                valor = valor * (-1)
                saida, created = Saida.objects.get_or_create(
                    descricao=descricao,
                    data_pagamento=data,
                    status='0',
                    valor_total=valor,
                    valor_liquido=valor,
                    abatimento='0.00',
                    juros='0.00',
                )
            else:
                entrada, created = Entrada.objects.get_or_create(
                    descricao=descricao,
                    data_pagamento=data,
                    status='0',
                    valor_total=valor,
                    valor_liquido=valor,
                    abatimento='0.00',
                    juros='0.00',
                )

            qtd += 1

        messages.success(request, "Importação de " + str(qtd) + " lançamentos realizada com sucesso!")



class AdicionarContaPagarView(AdicionarLancamentoBaseView):
    form_class = ContaPagarForm
    template_name = "financeiro/lancamento/lancamento_add.html"
    success_url = reverse_lazy('financeiro:listacontapagarview')
    success_message = "Conta a pagar <b>%(descricao)s </b>adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarContaPagarView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONTA A PAGAR'
        context['return_url'] = reverse_lazy('financeiro:listacontapagarview')
        return context


class AdicionarContaReceberView(AdicionarLancamentoBaseView):
    form_class = ContaReceberForm
    template_name = "financeiro/lancamento/lancamento_add.html"
    success_url = reverse_lazy('financeiro:listacontareceberview')
    success_message = "Conta a receber <b>%(descricao)s </b>adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarContaReceberView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONTA A RECEBER'
        context['return_url'] = reverse_lazy(
            'financeiro:listacontareceberview')
        return context


class AdicionarEntradaView(AdicionarLancamentoBaseView):
    form_class = EntradaForm
    template_name = "financeiro/lancamento/lancamento_add.html"
    success_url = reverse_lazy('financeiro:listarecebimentosview')
    success_message = "Recebimento <b>%(descricao)s </b>adicionado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarEntradaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR RECEBIMENTO'
        context['return_url'] = reverse_lazy(
            'financeiro:listarecebimentosview')
        return context


class AdicionarSaidaView(AdicionarLancamentoBaseView):
    form_class = SaidaForm
    template_name = "financeiro/lancamento/lancamento_add.html"
    success_url = reverse_lazy('financeiro:listapagamentosview')
    success_message = "Pagamento <b>%(descricao)s </b>adicionado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarSaidaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR PAGAMENTO'
        context['return_url'] = reverse_lazy('financeiro:listapagamentosview')
        return context


class AdicionarContaPagarPrestacaoView(CustomCreateView, MovimentoCaixaMixin):
    form_class = ContaPagarPrestacaoForm
    template_name = "financeiro/lancamento/lancamento_prestacao_add.html"
    success_url = reverse_lazy('financeiro:listacontapagarview')
    success_message = "Contas a pagar adicionadas com sucesso."
    permission_codename = 'add_lancamento'

    def get_context_data(self, **kwargs):
        context = super(AdicionarContaPagarPrestacaoView, self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONTA A PAGAR PARCELADA'
        context['return_url'] = reverse_lazy(
            'financeiro:listacontapagarview')
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = form_class(user=request.user)
        form.initial['data_pagamento'] = datetime.today().strftime('%d/%m/%Y')
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                    'juros' in key or
                    'abatimento' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = form_class(request.POST, user=request.user)

        if form.is_valid():
            self.object = form.save(commit=False)

            if self.object.movimentar_caixa:
                mvmt = None
                created = None

                quantidade_parcelas = int(request.POST['quantidade_parcelas'])
                valor_liquido = self.object.valor_liquido
                valor_parcela = round((valor_liquido / quantidade_parcelas), 2)
                resto = valor_liquido - (valor_parcela * quantidade_parcelas)
                valor_ultima_parcela = round((valor_parcela + resto), 2)

                for i in range(1, quantidade_parcelas + 1):
                    parcela = self.object

                    saida, created = Saida.objects.get_or_create(
                        data_emissao=parcela.data_emissao,
                        data_vencimento=parcela.primeiro_vencimento,
                        descricao=parcela.descricao + " (" + str(i) + "/" + str(quantidade_parcelas) + ")",
                        conta_corrente=parcela.conta_corrente,
                        depreciacao_bem=parcela.depreciacao_bem,
                        depreciacao_anos=parcela.depreciacao_anos,
                        valor_total=valor_ultima_parcela if i == quantidade_parcelas else valor_parcela,
                        abatimento=parcela.abatimento,
                        juros=parcela.juros,
                        valor_liquido=valor_ultima_parcela if i == quantidade_parcelas else valor_parcela,
                        movimento_caixa=parcela.movimento_caixa,
                        centro_custo=parcela.centro_custo,
                        fornecedor=parcela.fornecedor,
                        status=parcela.status,
                        grupo_plano=parcela.grupo_plano,
                        classificacao_dre=parcela.classificacao_dre,
                    )

                    if self.object.primeiro_vencimento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.primeiro_vencimento)

                    if mvmt:
                        if created:
                            self.atualizar_saldos(mvmt)

                        self.adicionar_novo_movimento_caixa(
                            lancamento=saida, novo_movimento=mvmt)
                        mvmt.save()
                        self.object.movimento_caixa = mvmt

                    if self.object.tipo_recorrencia == '1':
                        self.object.primeiro_vencimento = self.object.primeiro_vencimento + timedelta(days=self.object.recorrencia)
                    elif self.object.tipo_recorrencia == '2':
                        self.object.primeiro_vencimento = self.object.primeiro_vencimento + relativedelta(months=+self.object.recorrencia)
                    else:
                        self.object.primeiro_vencimento = self.object.primeiro_vencimento + relativedelta(years=+self.object.recorrencia)

            return self.form_valid(form)

        return self.form_invalid(form)


class AdicionarContaReceberPrestacaoView(CustomCreateView, MovimentoCaixaMixin):
    form_class = ContaReceberPrestacaoForm
    template_name = "financeiro/lancamento/lancamento_prestacao_add.html"
    success_url = reverse_lazy('financeiro:listacontareceberview')
    success_message = "Contas a receber adicionadas com sucesso."
    permission_codename = 'add_lancamento'

    def get_context_data(self, **kwargs):
        context = super(AdicionarContaReceberPrestacaoView,self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONTA A RECEBER PARCELADA'
        context['return_url'] = reverse_lazy(
            'financeiro:listacontareceberview')
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = form_class(user=request.user)
        form.initial['data_pagamento'] = datetime.today().strftime('%d/%m/%Y')
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                    'juros' in key or
                    'abatimento' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = form_class(request.POST, user=request.user)

        if form.is_valid():
            self.object = form.save(commit=False)

            if self.object.movimentar_caixa:
                mvmt = None
                created = None

                quantidade_parcelas = int(request.POST['quantidade_parcelas'])
                valor_liquido = self.object.valor_liquido
                valor_parcela = round((valor_liquido / quantidade_parcelas), 2)
                resto = valor_liquido - (valor_parcela * quantidade_parcelas)
                valor_ultima_parcela = round((valor_parcela + resto), 2)

                for i in range(1, quantidade_parcelas + 1):
                    parcela = self.object

                    entrada, created = Entrada.objects.get_or_create(
                        data_emissao=parcela.data_emissao,
                        data_vencimento=parcela.primeiro_vencimento,
                        descricao=parcela.descricao + " (" + str(i) + "/" + str(quantidade_parcelas) + ")",
                        conta_corrente=parcela.conta_corrente,
                        depreciacao_bem=parcela.depreciacao_bem,
                        depreciacao_anos=parcela.depreciacao_anos,
                        valor_total=valor_ultima_parcela if i == quantidade_parcelas else valor_parcela,
                        abatimento=parcela.abatimento,
                        juros=parcela.juros,
                        valor_liquido=valor_ultima_parcela if i == quantidade_parcelas else valor_parcela,
                        movimento_caixa=parcela.movimento_caixa,
                        centro_custo=parcela.centro_custo,
                        cliente=parcela.cliente,
                        status=parcela.status,
                        grupo_plano=parcela.grupo_plano,
                        classificacao_dre=parcela.classificacao_dre,
                    )

                    if self.object.primeiro_vencimento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.primeiro_vencimento)

                    if mvmt:
                        if created:
                            self.atualizar_saldos(mvmt)

                        self.adicionar_novo_movimento_caixa(
                            lancamento=entrada, novo_movimento=mvmt)
                        mvmt.save()
                        self.object.movimento_caixa = mvmt

                    if self.object.tipo_recorrencia == '1':
                        self.object.primeiro_vencimento = self.object.primeiro_vencimento + timedelta(days=self.object.recorrencia)
                    elif self.object.tipo_recorrencia == '2':
                        self.object.primeiro_vencimento = self.object.primeiro_vencimento + relativedelta(months=+self.object.recorrencia)
                    else:
                        self.object.primeiro_vencimento = self.object.primeiro_vencimento + relativedelta(years=+self.object.recorrencia)

            return self.form_valid(form)

        return self.form_invalid(form)


class EditarLancamentoBaseView(CustomUpdateView, MovimentoCaixaMixin):
    permission_codename = 'change_lancamento'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(instance=self.object, user=request.user)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                'juros' in key or
                    'abatimento' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        self.object = self.get_object()
        vliquido_previo = self.object.valor_liquido
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.object,
                          user=request.user)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            variacao_valor = self.object.valor_liquido - vliquido_previo

            if self.object.movimento_caixa:
                if self.object.movimentar_caixa:
                    mvmt = None
                    created = None
                    if self.object.data_pagamento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_pagamento)
                    elif self.object.data_vencimento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_vencimento)

                    # Inseriu uma data de pagamento ou vencimento
                    if mvmt:
                        # Caso seja o mesmo mvmt(mesmo id e data)
                        if mvmt.id == self.object.movimento_caixa.id:
                            self.adicionar_valor_movimento_caixa(
                                self.object, self.object.movimento_caixa, variacao_valor)

                        # Caso tenha mudado a data, criar outro objeto e checar
                        # se o antigo pode ser deletado
                        else:
                            self.remover_valor_movimento_caixa(
                                self.object, self.object.movimento_caixa, vliquido_previo)
                            if created:
                                self.atualizar_saldos(mvmt)
                            else:
                                mvmt.refresh_from_db()

                            self.adicionar_novo_movimento_caixa(
                                lancamento=self.object, novo_movimento=mvmt)
                            self.verificar_remocao_movimento(
                                self.object.movimento_caixa)

                            mvmt.save()
                            self.object.movimento_caixa = mvmt

                    # Nao inseriu(removeu) data de vencimento ou pagamento
                    else:
                        self.remover_valor_movimento_caixa(
                            self.object, self.object.movimento_caixa, vliquido_previo)
                        self.verificar_remocao_movimento(
                            self.object.movimento_caixa)
                        self.object.movimento_caixa = None

                # Retirou opcao de movimentar o caixa
                else:
                    self.remover_valor_movimento_caixa(
                        self.object, self.object.movimento_caixa, vliquido_previo)
                    self.verificar_remocao_movimento(
                        self.object.movimento_caixa)
                    self.object.movimento_caixa = None

            # Nao possui movimento de caixa previo
            else:
                # Decide movimentar o caixa
                if self.object.movimentar_caixa:
                    mvmt = None
                    created = None
                    if self.object.data_pagamento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_pagamento)
                    elif self.object.data_vencimento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_vencimento)

                    if mvmt:
                        if created:
                            self.atualizar_saldos(mvmt)

                        self.adicionar_novo_movimento_caixa(
                            lancamento=self.object, novo_movimento=mvmt)
                        mvmt.save()
                        self.object.movimento_caixa = mvmt

            self.object.save()
            return self.form_valid(form)

        return self.form_invalid(form)


class EditarContaPagarView(EditarLancamentoBaseView):
    form_class = ContaPagarForm
    model = Saida
    template_name = "financeiro/lancamento/lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listacontapagarview')
    success_message = "Conta a pagar <b>%(descricao)s </b>editada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarContaPagarView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('financeiro:listacontapagarview')
        return context


class EditarContaReceberView(EditarLancamentoBaseView):
    form_class = ContaReceberForm
    model = Entrada
    template_name = "financeiro/lancamento/lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listacontareceberview')
    success_message = "Conta a receber <b>%(descricao)s </b>editada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarContaReceberView,
                        self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'financeiro:listacontareceberview')
        return context


class EditarEntradaView(EditarLancamentoBaseView):
    form_class = EntradaForm
    model = Entrada
    template_name = "financeiro/lancamento/lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listarecebimentosview')
    success_message = "Recebimento <b>%(descricao)s </b>editado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarEntradaView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'financeiro:listarecebimentosview')
        return context


class EditarSaidaView(EditarLancamentoBaseView):
    form_class = SaidaForm
    model = Saida
    template_name = "financeiro/lancamento/lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listapagamentosview')
    success_message = "Pagamento <b>%(descricao)s </b>editado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarSaidaView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('financeiro:listapagamentosview')
        return context


class LancamentoListBaseView(CustomListView, MovimentoCaixaMixin):
    permission_codename = 'view_lancamento'

    def get_queryset(self, object, status):
        return object.objects.filter(status__in=status)

    # Remover items selecionados da database
    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, Lancamento):
            for key, value in request.POST.items():
                if value == "on":
                    instance = self.model.objects.get(id=key)
                    if(instance.movimento_caixa):
                        self.remover_valor_movimento_caixa(
                            instance, instance.movimento_caixa, instance.valor_liquido)
                        self.verificar_remocao_movimento(
                            instance.movimento_caixa)
                    instance.delete()
        return redirect(self.success_url)


class LancamentoListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    context_object_name = 'all_lancamentos'
    success_url = reverse_lazy('financeiro:listalancamentoview')

    def get_context_data(self, **kwargs):
        context = super(LancamentoListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'TODOS OS LANÇAMENTOS'
        context['all_lancamentos_saidas'] = Saida.objects.all()
        context['importar_lancamento_url'] = reverse_lazy(
            'financeiro:importarlancamentoview')
        return context

    def get_queryset(self):
        all_entradas = Entrada.objects.all()
        all_saidas = Saida.objects.all()
        all_lancamentos = list(chain(all_saidas, all_entradas))
        return all_lancamentos

    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, Lancamento):
            for key, value in request.POST.items():
                if value == "on":
                    if Entrada.objects.filter(id=key).exists():
                        instance = Entrada.objects.get(id=key)
                    elif Saida.objects.filter(id=key).exists():
                        instance = Saida.objects.get(id=key)
                    else:
                        raise ValueError(
                            'Entrada/Saida para o lancamento escolhido nao existe.')
                    if(instance.movimento_caixa):
                        self.remover_valor_movimento_caixa(
                            instance, instance.movimento_caixa, instance.valor_liquido)
                        self.verificar_remocao_movimento(
                            instance.movimento_caixa)
                    instance.delete()
        return redirect(self.success_url)


class ContaPagarListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    model = Saida
    context_object_name = 'all_contaspagar'
    success_url = reverse_lazy('financeiro:listacontapagarview')

    def get_context_data(self, **kwargs):
        context = super(ContaPagarListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A PAGAR'
        context['add_conta_pagar_url'] = reverse_lazy('financeiro:addcontapagarview')
        return context

    def get_queryset(self):
        return super(ContaPagarListView, self).get_queryset(object=Saida, status=['1', '2'])


class ContaPagarAtrasadasListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    model = Saida
    context_object_name = 'all_contaspagar'
    success_url = reverse_lazy('financeiro:listacontapagaratrasadasview')

    def get_context_data(self, **kwargs):
        context = super(ContaPagarAtrasadasListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A PAGAR ATRASADAS'
        context['add_conta_pagar_url'] = reverse_lazy('financeiro:addcontapagarview')
        return context

    def get_queryset(self):
        return Saida.objects.filter(data_vencimento__lt=datetime.now().date(), status__in=['1', '2'])


class ContaPagarHojeListView(ContaPagarAtrasadasListView):
    success_url = reverse_lazy('financeiro:listacontapagarhojeview')

    def get_context_data(self, **kwargs):
        context = super(ContaPagarHojeListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A PAGAR DO DIA ' + \
            datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('financeiro:addcontapagarview')
        return context

    def get_queryset(self):
        return Saida.objects.filter(data_vencimento=datetime.now().date(), status__in=['1', '2'])


class ContaReceberListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    model = Entrada
    context_object_name = 'all_contasreceber'
    success_url = reverse_lazy('financeiro:listacontareceberview')

    def get_context_data(self, **kwargs):
        context = super(ContaReceberListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A RECEBER'
        context['add_conta_receber_url'] = reverse_lazy('financeiro:addcontareceberview')
        return context

    def get_queryset(self):
        return super(ContaReceberListView, self).get_queryset(object=Entrada, status=['1', '2'])


class ContaReceberAtrasadasListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    model = Entrada
    context_object_name = 'all_contasreceber'
    success_url = reverse_lazy('financeiro:listacontareceberatrasadasview')

    def get_context_data(self, **kwargs):
        context = super(ContaReceberAtrasadasListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A RECEBER ATRASADAS'
        context['add_conta_receber_url'] = reverse_lazy('financeiro:addcontareceberview')
        return context

    def get_queryset(self):
        return Entrada.objects.filter(data_vencimento__lt=datetime.now().date(), status__in=['1', '2'])


class ContaReceberHojeListView(ContaReceberAtrasadasListView):
    success_url = reverse_lazy('financeiro:listacontareceberhojeview')

    def get_context_data(self, **kwargs):
        context = super(ContaReceberHojeListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A RECEBER DO DIA ' + \
            datetime.now().date().strftime('%d/%m/%Y')
        context['add_conta_receber_url'] = reverse_lazy('financeiro:addcontareceberview')
        return context

    def get_queryset(self):
        return Entrada.objects.filter(data_vencimento=datetime.now().date(), status__in=['1', '2'])


class EntradaListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    model = Entrada
    context_object_name = 'all_entradas'
    success_url = reverse_lazy('financeiro:listarecebimentosview')

    def get_context_data(self, **kwargs):
        context = super(EntradaListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'RECEBIMENTOS'
        context['add_recebimento_url'] = reverse_lazy('financeiro:addrecebimentoview')
        return context

    def get_queryset(self):
        return super(EntradaListView, self).get_queryset(object=Entrada, status=['0', ])


class SaidaListView(LancamentoListBaseView):
    template_name = 'financeiro/lancamento/lancamento_list.html'
    model = Saida
    context_object_name = 'all_saidas'
    success_url = reverse_lazy('financeiro:listapagamentosview')

    def get_context_data(self, **kwargs):
        context = super(SaidaListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'PAGAMENTOS'
        context['add_pagamento_url'] = reverse_lazy('financeiro:addpagamentoview')
        return context

    def get_queryset(self):
        return super(SaidaListView, self).get_queryset(object=Saida, status=['0', ])


class GerarLancamentoView(CustomView, MovimentoCaixaMixin):
    permission_codename = ['add_lancamento', 'change_lancamento']

    def post(self, request, *args, **kwargs):
        conta_id = request.POST['contaId']
        data = {}

        # Tipo conta: 0 = Receber, 1 = Pagar
        if request.POST['tipoConta'] == '0':
            obj = Entrada.objects.get(id=conta_id)
            data['url'] = reverse_lazy(
                'financeiro:editarrecebimentoview', kwargs={'pk': obj.id})
            obj.status = '0'
            obj.data_pagamento = datetime.strptime(
                request.POST['dataPagamento'], '%d/%m/%Y').strftime('%Y-%m-%d')
            obj.save()
            if obj.movimentar_caixa:
                self.atualizar_movimento_caixa(obj)
        elif request.POST['tipoConta'] == '1':
            obj = Saida.objects.get(id=conta_id)
            data['url'] = reverse_lazy(
                'financeiro:editarpagamentoview', kwargs={'pk': obj.id})
            obj.status = '0'
            obj.data_pagamento = datetime.strptime(
                request.POST['dataPagamento'], '%d/%m/%Y').strftime('%Y-%m-%d')
            obj.save()
            if obj.movimentar_caixa:
                self.atualizar_movimento_caixa(obj)

        return JsonResponse(data)

    def atualizar_movimento_caixa(self, object):
        mvmt = None
        created = None
        if object.data_pagamento:
            mvmt, created = MovimentoCaixa.objects.get_or_create(
                data_movimento=object.data_pagamento)

        if mvmt:
            # Caso a data esteja trocada
            if mvmt.id != object.movimento_caixa.id:
                # Atualizar os valores sem o movimento antigo
                self.remover_valor_movimento_caixa(
                    object, object.movimento_caixa, object.valor_liquido)
                if created:
                    self.atualizar_saldos(mvmt)
                else:
                    mvmt.refresh_from_db()

                self.verificar_remocao_movimento(object.movimento_caixa)
                self.adicionar_novo_movimento_caixa(
                    lancamento=object, novo_movimento=mvmt)

                mvmt.save()
                object.movimento_caixa = mvmt
                object.save()


class FaturarPedidoVendaView(CustomView, MovimentoCaixaMixin):
    permission_codename = 'vendas.faturar_pedidovenda'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def atualizar_estoque(self, request, pedido):
        erros = False
        lista_prod_estocado = []
        lista_itens_saida = []

        # Gerar o ProdutoEstocado e ItensMovimento para cada produto com controle_estoque=True
        # Modificar o valor de estoque_atual de cada produto
        for item in pedido.itens_venda.all():
            if item.produto.controlar_estoque:
                try:
                    prod_estocado = ProdutoEstocado.objects.get(
                        local=pedido.local_orig, produto=item.produto)
                    if item.quantidade > item.produto.estoque_atual:
                        erros = True
                        messages.warning(request, 'Aviso: A venda não pode ser faturada. O estoque atual do produto ' + str(item.produto.descricao)
                                         + ' é de apenas ' + str(item.produto.estoque_atual))
                    elif item.quantidade > prod_estocado.quantidade:
                        erros = True
                        messages.warning(request, 'Aviso: A venda não pode ser faturada. O estoque atual do produto ' + str(item.produto.descricao) +
                                         ' no local ' + str(pedido.local_orig) + ' é de apenas ' + str(prod_estocado.quantidade))
                    elif not erros:
                        item_mvmt = ItensMovimento()
                        item_mvmt.produto = item.produto
                        item_mvmt.quantidade = item.quantidade
                        item_mvmt.valor_unit = item.valor_unit
                        item_mvmt.subtotal = item.vprod
                        lista_itens_saida.append(item_mvmt)
                        prod_estocado.produto.estoque_atual -= item.quantidade
                        prod_estocado.produto.quantidade_vendida += item.quantidade
                        prod_estocado.quantidade -= item.quantidade
                        lista_prod_estocado.append(prod_estocado)

                except ProdutoEstocado.DoesNotExist:
                    erros = True
                    messages.warning(request, 'Aviso: A venda não pode ser faturada. O estoque atual do produto ' + str(item.produto.descricao) +
                                     ' no local ' + str(pedido.local_orig) + ' é 0,00')

        # Salvar se nao ocorreu erros
        if not erros:
            saida_estoque = SaidaEstoque()
            saida_estoque.data_movimento = pedido.data_entrega
            saida_estoque.quantidade_itens = pedido.itens_venda.count()
            saida_estoque.observacoes = 'Saída de estoque pelo pedido de venda nº{}'.format(
                str(pedido.id))
            saida_estoque.tipo_movimento = u'1'
            saida_estoque.valor_total = pedido.get_total_produtos_estoque()
            saida_estoque.pedido_venda = pedido
            saida_estoque.local_orig = pedido.local_orig

            saida_estoque.save()

            for i in lista_itens_saida:
                i.movimento_id = saida_estoque
                i.save()

            for p in lista_prod_estocado:
                p.produto.save()
                p.save()

        return erros

    def get(self, request, *args, **kwargs):
        pedido_id = kwargs.get('pk', None)
        pedido = PedidoVenda.objects.get(id=pedido_id)
        pagamentos = pedido.parcela_pagamento.all()
        n_parcelas = pagamentos.count()

        if pedido.movimentar_estoque:
            if self.atualizar_estoque(request, pedido):
                return redirect(request.META['HTTP_REFERER'])

        cliente = Cliente.objects.filter(id=pedido.cliente.id).get()
        total = 0

        for pagamento in pagamentos:
            entrada = Entrada()
            entrada.cliente = pedido.cliente
            entrada.status = '1'
            entrada.data_vencimento = pagamento.vencimento
            entrada.descricao = 'Parcela {0}/{1} - Pedido de venda nº{2}'.format(
                str(pagamento.indice_parcela), str(n_parcelas), str(pedido.id))
            entrada.valor_total = pagamento.valor_parcela
            entrada.valor_liquido = pagamento.valor_parcela
            entrada.save()
            total += pagamento.valor_parcela
            mvmt = None
            created = None
            if pagamento.vencimento:
                mvmt, created = MovimentoCaixa.objects.get_or_create(
                    data_movimento=pagamento.vencimento)

            if mvmt:
                if created:
                    self.atualizar_saldos(mvmt)

                self.adicionar_novo_movimento_caixa(
                    lancamento=entrada, novo_movimento=mvmt)
                mvmt.save()
                entrada.movimento_caixa = mvmt
                entrada.save()

        cliente.valor_total_vendas += total
        cliente.save()

        pedido.status = '1'
        pedido.save()

        messages.success(
            request, "<b>Pedido de venda {0} </b>faturado com sucesso.".format(str(pedido.id)))

        return redirect(reverse_lazy('vendas:listapedidovendaview'))


class FaturarPedidoCompraView(CustomView, MovimentoCaixaMixin):
    permission_codename = 'compras.faturar_pedidocompra'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        pedido_id = kwargs.get('pk', None)
        pedido = PedidoCompra.objects.get(id=pedido_id)
        pagamentos = pedido.parcela_pagamento.all()
        n_parcelas = pagamentos.count()

        for pagamento in pagamentos:
            saida = Saida()
            saida.fornecedor = pedido.fornecedor
            saida.status = '1'
            saida.data_vencimento = pagamento.vencimento
            saida.descricao = 'Parcela {0}/{1} - Pedido de compra nº{2}'.format(
                str(pagamento.indice_parcela), str(n_parcelas), str(pedido.id))
            saida.valor_total = pagamento.valor_parcela
            saida.valor_liquido = pagamento.valor_parcela
            saida.save()
            mvmt = None
            created = None
            if pagamento.vencimento:
                mvmt, created = MovimentoCaixa.objects.get_or_create(
                    data_movimento=pagamento.vencimento)

            if mvmt:
                if created:
                    self.atualizar_saldos(mvmt)

                self.adicionar_novo_movimento_caixa(
                    lancamento=saida, novo_movimento=mvmt)
                mvmt.save()
                saida.movimento_caixa = mvmt
                saida.save()

        pedido.status = '1'
        pedido.save()

        messages.success(
            request, "<b>Pedido de compra {0} </b>realizado com sucesso.".format(str(pedido.id)))

        return redirect(reverse_lazy('compras:listapedidocompraview'))
