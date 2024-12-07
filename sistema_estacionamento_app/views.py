from datetime import datetime
import random, time
from http import client
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F, Q

from sistema_estacionamento_app.models import Precos

def home(request):
    return render(request, "sistema_estacionamento/home.html")

def precoePromocao(request):
    # Ordena os registros de Precos pela data de início (dataInic) de forma crescente
    precos_ativos = Precos.objects.filter(dataFim__gte=timezone.now().date()).order_by('dataInic')

    precos_com_conflito = []

    if request.method == "POST":
        dtinic = request.POST.get('dataInic')
        dtfim = request.POST.get('dataFim')
        valor_preco = request.POST.get('valorPreco')

        try:
            # Converte as strings para objetos de data
            data_inic = datetime.strptime(dtinic, "%Y-%m-%d").date()
            data_fim = datetime.strptime(dtfim, "%Y-%m-%d").date()

            # Verifica conflitos de datas
            conflitos = Precos.objects.filter(
                models.Q(dataInic__lte=data_fim) & models.Q(dataFim__gte=data_inic)
            )

            if conflitos.exists():
                # Se houver conflito, armazene os registros conflitantes
                precos_com_conflito = conflitos

                raise ValueError("O intervalo de datas se sobrepõe a um registro existente.")

            # Se não houver conflito, cria um novo registro
            Precos.objects.create(dataInic=data_inic, dataFim=data_fim, valorPreco=float(valor_preco))

            # Variável de sucesso para passar para o template
            success_message = "Registro inserido com sucesso!"

            # Redireciona para a mesma página com a mensagem de sucesso
            return render(request, "sistema_estacionamento/precoepromocao.html", {
                "success_message": success_message,
                "precos_ativos": precos_ativos,
                "precos_com_conflito": precos_com_conflito,
            })

        except Exception as e:
            # Tratamento de erros
            return render(request, "sistema_estacionamento/precoepromocao.html", {
                "error_message": f"Erro ao salvar os dados: {str(e)}",
                "precos_ativos": precos_ativos,
                "precos_com_conflito": precos_com_conflito,
            })

    return render(request, "sistema_estacionamento/precoepromocao.html", {
        "precos_ativos": precos_ativos,
        "precos_com_conflito": precos_com_conflito,
    })