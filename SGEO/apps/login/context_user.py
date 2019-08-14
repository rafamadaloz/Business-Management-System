# -*- coding: utf-8 -*-

from .models import Usuario
from SGEO.apps.cadastro.models import MinhaEmpresa
from SGEO.apps.boletos.models import ConfiguracaoBoleto


# Manter foto do perfil na sidebar


def foto_usuario(request):
    context_dict = {}
    # Foto do usuario
    try:
        user_foto = Usuario.objects.get(user=request.user).user_foto
        context_dict['user_foto_sidebar'] = user_foto
        user_capa_foto = Usuario.objects.get(user=request.user).user_capa_foto
        context_dict['user_capa_foto_sidebar'] = user_capa_foto
    except:
        pass

    # Empresa do usuario
    try:
        user_empresa = MinhaEmpresa.objects.get(
            m_usuario=Usuario.objects.get(user=request.user)).m_empresa
        if user_empresa:
            context_dict['user_empresa'] = user_empresa
    except:
        pass

    try:
        context_dict['configuracao_boletos'] = ConfiguracaoBoleto.objects.last()
    except:
        context_dict['configuracao_boletos'] = False


    return context_dict
