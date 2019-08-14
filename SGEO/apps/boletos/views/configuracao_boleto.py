# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
from SGEO.apps.base.custom_views import CustomCreateView, CustomUpdateView
from SGEO.apps.boletos.models import ConfiguracaoBoleto
from SGEO.apps.boletos.forms import ConfiguracoesBoletoForm


class AdicionarConfiguracaoBoletoView(CustomCreateView):
    template_name = "boletos/configuracao/adicionar_configuracao.html"
    form_class = ConfiguracoesBoletoForm
    model = ConfiguracaoBoleto
    # success_url = reverse('boletos:editarconfiguracaoboletoview', args=(object.id,))
    # obj = ConfiguracaoBoleto.objects.all().count()
    # if obj > 0:
    #     obj = ConfiguracaoBoleto.objects.latest('id')
    #     success_url = reverse_lazy('boletos:editarconfiguracaoboletoview', kwargs={'pk': obj.id})
    # success_message = "Configuração de boleto editada com sucesso!"
    permission_codename = 'add_configuracaoboleto'

    def get_success_url(self):
        return reverse('boletos:editarconfiguracaoboletoview', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(AdicionarConfiguracaoBoletoView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Adicionar Configuração de Boleto'
        return context


class EditarConfiguracaoBoletoView(CustomUpdateView):
    template_name = "boletos/configuracao/editar_configuracao.html"
    form_class = ConfiguracoesBoletoForm
    model = ConfiguracaoBoleto
    # success_url = reverse('rboletos:editarconfiguracaoboletoview', kwargs={'pk': self.object.pk})
    # obj = ConfiguracaoBoleto.objects.all().count()
    # if obj > 0:
    #     obj = ConfiguracaoBoleto.objects.latest()z
    #     success_url = reverse_lazy('boletos:editarconfiguracaoboletoview', kwargs={'pk': obj.id})

    permission_codename = 'change_configuracaoboleto'
    success_message = "Configuração de boleto editada com sucesso!"

    # def get_success_url(self):
    #     return reverse('rboletos:editarconfiguracaoboletoview', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EditarConfiguracaoBoletoView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Editar Configuração de Boleto'
        return context