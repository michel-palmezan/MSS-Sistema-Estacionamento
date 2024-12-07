#from distutils.archive_util import make_zipfile
from xml.parsers.expat import model
from django.db import models
from django.forms import CharField, Field
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
import datetime


# ****** Definição da classe Precos
class Precos(models.Model):
    #lista de atributos com os tipos que vão ser armazenados no nosso banco de dadps
    dataInic = models.DateField()
    dataFim = models.DateField()
    valorPreco = models.FloatField()
    
    # ********** Métodos da classe **********
    
    def registrarPreco(self):
        #salva no banco as infos contidas no objeto que chamou o método (self)
        self.save()
        
    def clean(self):
        
        #Valida se as datas de início e fim não sobrepõem outras entradas no banco.
        
        # Valida se `dataInic` é menor ou igual a `dataFim`
        if self.dataInic > self.dataFim:
            raise ValidationError("A data inicial deve ser anterior ou igual à data final.")

        # Consulta para verificar sobreposições
        overlapping_entries = Precos.objects.filter(
            models.Q(dataInic__lte=self.dataFim) & models.Q(dataFim__gte=self.dataInic)
        )

        # Excluir a si mesmo da consulta (caso seja uma atualização)
        if self.pk:
            overlapping_entries = overlapping_entries.exclude(pk=self.pk)

        if overlapping_entries.exists():
            raise ValidationError("O intervalo de datas se sobrepõe a um registro existente.")

    def save(self, *args, **kwargs):
        
        #Garante que a validação seja executada antes de salvar.
        
        self.clean()  # Executa validação
        super().save(*args, **kwargs)
    
