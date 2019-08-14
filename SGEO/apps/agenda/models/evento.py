from django.db import models
from django.urls import reverse


COR_ESCOLHAR = [
    ('#FFD700', 'Amarelo'),
    ('#0071c5', 'Azul Turquesa'),
    ('#FF4500', 'Laranja'),
    ('#8B4513', 'Marrom'),
    ('#1C1C1C', 'Preto'),
    ('#436EEE', 'Royal Blue'),
    ('#A020F0', 'Roxo'),
    ('#40E0D0', 'Turquesa'),
    ('#228B22', 'Verde'),
    ('#8B0000', 'Vermelho')
]

class Events(models.Model):
    event_name = models.CharField(max_length=255, null=True, blank=True)
    cor = models.CharField(
        max_length=10, choices=COR_ESCOLHAR, default='#0071c5')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = "Agenda"
        permissions = (
            ("acesso_events", "Pode acessar a agenda"),
        )
