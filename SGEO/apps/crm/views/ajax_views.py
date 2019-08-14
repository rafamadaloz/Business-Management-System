# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse

import json

from SGEO.apps.crm.models import Oportunidade

class InfoOportunidade(View):

    def post(self, request, *args, **kwargs):
        oportunidade = Oportunidade.objects.get(pk=request.POST['oportunidadeID'])

        data = []



        return HttpResponse(json.dumps(data), content_type='application/json')