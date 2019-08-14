# -*- coding: utf-8 -*-
from SGEO.apps.base.custom_views import CustomCreateView
from django.views.generic import TemplateView
from django.shortcuts import render
from SGEO.apps.agenda.models import Events
from SGEO.apps.agenda.forms import EventsForm
from django.urls import reverse_lazy

class AgendaView2(TemplateView):
    template_name = 'agenda/agenda.html'


class AgendaView(CustomCreateView):

    form_class = EventsForm
    template_name = "agenda/agenda.html"
    success_url = reverse_lazy('agenda:agendaview')
    success_message = "<b>Evento %(id)s </b>adicionado com sucesso."
    permission_codename = 'acesso_events'

    def get_context_data(self, **kwargs):
        context = super(AgendaView, self).get_context_data(**kwargs)
        context['eventos'] = Events.objects.all()
        context['teste'] = 'teste'
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AgendaView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AgendaView, self).post(request, form_class, *args, **kwargs)


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


#def event(request):
    #all_events = Events.objects.all()
  #  get_event_types = Events.objects.only('event_type')

    # if filters applied then get parameter and filter based on condition else return object
   # if request.GET:
    #    event_arr = []
     #   if request.GET.get('event_type') == "all":
      #      all_events = Events.objects.all()
       ###
        #for i in all_events:
         #   event_sub_arr = {}
          #  event_sub_arr['title'] = i.event_name
           # start_date = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            #end_date = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
       #     event_sub_arr['start'] = start_date
        #    event_sub_arr['end'] = end_date
         #   event_arr.append(event_sub_arr)
        #return HttpResponse(json.dumps(event_arr))

   # context = {
  ##
  #  }
   # return render(request, 'agenda/agenda.html', context)
##