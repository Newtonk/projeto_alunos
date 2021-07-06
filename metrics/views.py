import json
from io import BytesIO

from django.contrib.auth import logout
from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from metrics.entities.pageGender.graph_genero_vs_dados_empresariais import *
from metrics.entities.pageGender.graph_comparativo_genero_vs_dados_empresariais import *
from metrics.entities.pageSocialClass.graph_class_vs_dados_empresariais import *
from metrics.entities.pageSocialClass.graph_comparativo_class_vs_dados_empresariais import *
from metrics.entities.pageSallary.graph_comparativo_sallary_vs_dados import *
from metrics.entities.pageAge.graph_comparativo_age_vs_dados import *
from metrics.entities.pageQuantity.graph_comparativo_quantity_vs_dados import *


def home(request):
    global context

    context = {}
    contextHome = {}

    if request.method == 'POST':
        if 'File' not in request.FILES:
            messages.info(request, "Nenhum arquivo enviado! Por favor, envie um arquivo .csv ou .xlsx")
            return render(request, 'metrics/home.html', contextHome)
        file = request.FILES['File']
        fileList = file.name.split('.')
        if len(fileList) > 0:
            extension = fileList[-1]
            if extension != "csv" and extension != "xlsx":
                messages.info(request, "Arquivo de envio não está no formato correto(.csv ou .xlsx)")
                return render(request, 'metrics/home.html', contextHome)
        else:
            messages.info(request, "Arquivo de envio está corrompido!")
            return render(request, 'metrics/home.html', contextHome)
        success = read_file_success(file, extension)
        if not success:
            messages.info(request, "Arquivo de envio está corrompido!")
            return render(request, 'metrics/home.html', contextHome)

        # pre_validations()
        return graphs_genero(request)


    return render(request, 'metrics/home.html', contextHome)

def pre_validations():
    if check_minium_values(["Curso"], data):
        data.loc[data['Curso'].str.contains("SISTEMA", na=False), "Curso"] = "SISTEMAS"
        data.loc[data['Curso'].str.contains("ENGENHARIA", na=False), "Curso"] = "ENGENHARIA"
        data.loc[data['Curso'].str.contains("COMPUTACAO", na=False), "Curso"] = "COMPUTACAO"
        data.loc[(data['Curso'] != "SISTEMAS") & (data['Curso'] != "ENGENHARIA") & (data['Curso'] != "COMPUTACAO"), "Curso"] = "OUTROS CURSOS DE TI"

def read_file_success(fileName, fileExtension):
    global data
    try:
        myFile = None
        if fileExtension == "csv":
            myFile = pd.read_csv(fileName, chunksize=10000000)
        elif fileExtension == "xlsx":
            myFile = pd.read_excel(fileName)
        for df in myFile:
            data = pd.DataFrame(data=df, index=None)
            break;
    except:
        return False
    return True

def logoutUser(request):
	logout(request)
	return redirect('home')

def update_graph(request):
    graph_name = request.POST["graph_name"]

    if graph_name == "generoXmercadodetrabalho":
        context["generoXmercadodetrabalho"] = graph_genero_vs_mercado_trabalho(request)
    elif graph_name == "generoXmercadodetrabalhoCompare":
        context["generoXmercadodetrabalhoCompare"] = graph_genero_vs_mercado_trabalho_comparativo(request)
    elif graph_name == "classeXmercadodetrabalho":
        context["classeXmercadodetrabalho"] = graph_classe_vs_mercado_trabalho(request)
    elif graph_name == "classeXmercadodetrabalhoCompare":
        context["classeXmercadodetrabalhoCompare"] = graph_classe_vs_mercado_trabalho_comparativo(request)
    elif graph_name == "salarioXdadosCompare":
        context["salarioXdadosCompare"] = graph_salario_vs_dados_compare(request)
    elif graph_name == "idadeXdadosCompare":
        context["idadeXdadosCompare"] = graph_age_vs_dados_compare(request)
    elif graph_name == "quantidadeXdadosCompare":
        context["quantidadeXdadosCompare"] = graph_quantity_vs_dados_compare(request)

    return JsonResponse(context, safe=False)

#region Gráficos de Genero

def graphs_genero(request):
    context["generoXmercadodetrabalho"] = None
    context["generoXmercadodetrabalhoCompare"] = None

    generoXmercadodetrabalho = graph_genero_vs_mercado_trabalho(request)

    generoXmercadodetrabalhoCompare = graph_genero_vs_mercado_trabalho_comparativo(request)

    context["generoXmercadodetrabalho"] = generoXmercadodetrabalho
    context["generoXmercadodetrabalhoCompare"] = generoXmercadodetrabalhoCompare

    return render(request, 'metrics/pageGender/graphs_gender.html', context)

def graph_genero_vs_mercado_trabalho(request):
    finalResult = {}
    if GeneroDadosEmpresariais.validacao_colunas(data):
        workingData = data
        newData = GeneroDadosEmpresariais.unifica_colunas(workingData)
        finalResult, dataInfo, noInfo = GeneroDadosEmpresariais.valida_dados_enviados(newData, request, context)

        listTotal = []
        indexes = []
        if not noInfo:
            if len(dataInfo.index.names) > 1:
                position = dataInfo.index.names.index("Genero")
                listLabels = dataInfo.index.levels[position].values.tolist()
                indexes = dataInfo.index.levels[position]
            elif len(dataInfo.index.names) == 1:
                listLabels = dataInfo.index.values.tolist()
                indexes = dataInfo.index

            listLabels = [x for x in listLabels if str(x) != 'nan']
            if len(listLabels) > 0:
                for index in indexes:
                    if index in dataInfo:
                        sum = 0
                        if len(dataInfo.index.names) > 1:
                            sum = int(dataInfo[index].values.sum())
                        elif len(dataInfo.index.names) == 1:
                            sum = int(dataInfo[index].sum())
                        listTotal.append(sum)
                    elif index in listLabels:
                        listLabels.remove(index)
        finalResult["Labels"] = listLabels
        finalResult["Data"] = listTotal

    return finalResult

def graph_genero_vs_mercado_trabalho_comparativo(request):
    finalResult = {}
    if GeneroDadosComparativosEmpresariais.validacao_colunas(data):
        workingData = data
        newData = GeneroDadosComparativosEmpresariais.unifica_colunas(workingData)
        finalResult, complementData, finalData, noInfo = GeneroDadosComparativosEmpresariais.valida_dados_enviados(newData, request, context)

        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Entity"] = index
                area_frame = complementData['Count'][index]
                total_people = area_frame.sum()
                if finalResult["Gender"][0] in area_frame:
                    result["GenderValue"] = (int(area_frame[finalResult["Gender"][0]]) * 100) / total_people
                    all_values.append(result)
            if len(all_values) > 0:
                if finalResult["Order"] == "Max":
                    all_values.sort(key=lambda x: x["GenderValue"], reverse=True)
                else:
                    all_values.sort(key=lambda x: x["GenderValue"])

                list_entities = list(o["Entity"] for o in all_values)
                list_values = list(o["GenderValue"] for o in all_values)

        finalResult["Entities"] = list_entities
        finalResult["Data"] = list_values

    return finalResult
#endregion

#region Gráficos de Classe Social

def graphs_social_class(request):
    context["classeXmercadodetrabalho"] = None
    context["classeXmercadodetrabalhoCompare"] = None

    classeXmercadodetrabalho = graph_classe_vs_mercado_trabalho(request)

    classeXmercadodetrabalhoCompare = graph_classe_vs_mercado_trabalho_comparativo(request)

    context["classeXmercadodetrabalho"] = classeXmercadodetrabalho
    context["classeXmercadodetrabalhoCompare"] = classeXmercadodetrabalhoCompare

    return render(request, 'metrics/pageSocialClass/graphs_social_class.html', context)

def graph_classe_vs_mercado_trabalho(request):
    finalResult = {}
    if ClasseDados.validacao_colunas(data):
        workingData = data
        newData = ClasseDados.unifica_colunas(workingData)
        finalResult, dataValue, noInfo = ClasseDados.valida_dados_enviados(newData, request, context)

        listTotal = []
        indexes = []
        if not noInfo:
            if len(dataValue.index.names) > 1:
                position = dataValue.index.names.index("Classe")
                listLabels = dataValue.index.levels[position].values.tolist()
                indexes = dataValue.index.levels[position]
            elif len(dataValue.index.names) == 1:
                listLabels = dataValue.index.values.tolist()
                indexes = dataValue.index

            listLabels = [x for x in listLabels if str(x) != 'nan']
            if len(listLabels) > 0:
                for index in indexes:
                    if index in dataValue:
                        sum = 0
                        if len(dataValue.index.names) > 1:
                            sum = int(dataValue[index].values.sum())
                        elif len(dataValue.index.names) == 1:
                            sum = int(dataValue[index].sum())
                        listTotal.append(sum)
                    elif index in listLabels:
                        listLabels.remove(index)

        finalResult["Labels"] = listLabels
        finalResult["Data"] = listTotal
    return finalResult

def graph_classe_vs_mercado_trabalho_comparativo(request):
    finalResult = {}
    if ClasseDadosComparativos.validacao_colunas(data):
        workingData = data
        newData = ClasseDadosComparativos.unifica_colunas(workingData)
        finalResult, complementData, finalData, noInfo = ClasseDadosComparativos.valida_dados_enviados(newData, request,
                                                                                                      context)

        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Entity"] = index
                area_frame = complementData['Count'][index]
                total_people = area_frame.sum()
                if finalResult["Class"][0] in area_frame:
                    result["ClassValue"] = (int(area_frame[finalResult["Class"][0]]) * 100) / total_people
                    all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["ClassValue"], reverse=True)

                list_entities = list(o["Entity"] for o in all_values)
                list_values = list(o["ClassValue"] for o in all_values)

        finalResult["Entities"] = list_entities
        finalResult["Data"] = list_values

    return finalResult
#endregion

#region Gráficos de Salario

def graphs_sallary(request):
    context["salarioXdadosCompare"] = None

    salarioXdadosCompare = graph_salario_vs_dados_compare(request)

    context["salarioXdadosCompare"] = salarioXdadosCompare

    return render(request, 'metrics/pageSallary/graphs_sallary.html', context)

def graph_salario_vs_dados_compare(request):
    finalResult = {}
    if SalarioDadosComparativos.validacao_colunas(data):
        workingData = data
        newData = SalarioDadosComparativos.unifica_colunas(workingData)
        finalResult, complementData, finalData, noInfo = SalarioDadosComparativos.valida_dados_enviados(newData, request, context)

        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Entity"] = index
                total_sallary = complementData["Salario"][index]
                result["SallaryValue"] = int(total_sallary) / value
                all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["SallaryValue"], reverse=True)

                list_entities = list(o["Entity"] for o in all_values)
                list_values = list(o["SallaryValue"] for o in all_values)

        finalResult["Entities"] = list_entities
        finalResult["Data"] = list_values
    return finalResult
#endregion

#region Gráficos de Idade

def graphs_age(request):
    context["idadeXdadosCompare"] = None

    idadeXdadosCompare = graph_age_vs_dados_compare(request)

    context["idadeXdadosCompare"] = idadeXdadosCompare

    return render(request, 'metrics/pageAge/graphs_age.html', context)

def graph_age_vs_dados_compare(request):
    finalResult = {}
    if IdadeDadosComparativos.validacao_colunas(data):
        workingData = data
        newData = IdadeDadosComparativos.unifica_colunas(workingData)
        finalResult, complementData, finalData, noInfo = IdadeDadosComparativos.valida_dados_enviados(newData, request,
                                                                                                       context)

        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Entity"] = index
                total_age = complementData["Idade"][index]
                result["AgeValue"] = int(total_age) / value
                all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["AgeValue"], reverse=True)

                list_entities = list(o["Entity"] for o in all_values)
                list_values = list(o["AgeValue"] for o in all_values)

        finalResult["Entities"] = list_entities
        finalResult["Data"] = list_values
    return finalResult

#endregion

#region Gráficos de Quantidade

def graphs_quantity(request):
    context["quantidadeXdadosCompare"] = None

    quantidadeXdadosCompare = graph_quantity_vs_dados_compare(request)

    context["quantidadeXdadosCompare"] = quantidadeXdadosCompare

    return render(request, 'metrics/pageQuantity/graphs_quantity.html', context)

def graph_quantity_vs_dados_compare(request):
    finalResult = {}
    if QuantidadeDadosComparativos.validacao_colunas(data):
        workingData = data
        newData = QuantidadeDadosComparativos.unifica_colunas(workingData)
        finalResult, finalData, noInfo = QuantidadeDadosComparativos.valida_dados_enviados(newData, request, context)

        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Entity"] = index
                result["Quantity"] = int(value)
                all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["Quantity"], reverse=True)

                list_entities = list(o["Entity"] for o in all_values)
                list_values = list(o["Quantity"] for o in all_values)

        finalResult["Entities"] = list_entities
        finalResult["Data"] = list_values

    return finalResult


#endregion