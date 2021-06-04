import base64
from io import BytesIO, StringIO

from PIL import Image
from django.shortcuts import render, redirect
import pandas as pd
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

data = None

global context
context = {
    "generoXcurso": None,
    "generoXuniversidade" : None,
    "generoXarea": None,
    "ageXarea" : None,
    "generoXsalario" : None,
    "areaXcurso" : None,
    "universidadeXempresa" : None
}


def home(request):
    context = {}
    if request.method == 'POST':
        filename = request.FILES['File']
        read_csv(filename)
        return graphs_profissionais_vs_universidade(request)

    return render(request, 'metrics/home.html', context)

def read_csv(filename):
    global data

    myFile = pd.read_csv(BytesIO(filename.read()))

    data = pd.DataFrame(data=myFile, index=None)

#region Universidade vs Empresa ( Area X Curso , ...)
def graphs_universidade_vs_empresa(request):
    areaXcurso = graph_area_vs_curso()

    universidadeXempresa = graph_university_vs_company(request)

    context["areaXcurso"] = areaXcurso

    context["universidadeXempresa"] = universidadeXempresa

    return render(request, 'metrics/graphs_universidade_vs_empresa.html', context)

def graph_area_vs_curso():
    counter = data.groupby(['Curso', 'Area']).size().reset_index(name='Count')
    df_new = counter.groupby(['Curso', 'Area']).sum()
    df_new = df_new.sort_values(by=['Count'], ascending=False)

    countValues = df_new['Count']
    finalResult = []
    for index, value in countValues.groupby(level=0):
        areas_values = countValues[index].nlargest(10)
        areas = areas_values.index.tolist()
        numbers = areas_values.values.tolist()
        result = {}
        result["Label"] = index
        result["Areas"] = areas
        result["Valores"] = numbers
        finalResult.append(result)
    return finalResult

def graph_university_vs_company(request):
    firstColumn = ""
    secondColumn = ""
    choosedEntity = ""
    choosedValue = ""
    total = 0
    if 'qtyuniversitycompany' in request.POST:
        total = int(request.POST['qtyuniversitycompany'])
    elif context["universidadeXempresa"] is None:
        total = 10
    else:
        total = context["universidadeXempresa"]["Total"]
    # Choose which element we want to see ( Companys or Universitys) as main element
    if 'universityorcompany' in request.POST:
        choosedEntity = request.POST['universityorcompany']
    elif context["universidadeXempresa"] is None:
        choosedEntity = "Empresas"
    else:
        choosedEntity = context["universidadeXempresa"]["ChoosedEntity"]
    if choosedEntity == "Empresas":
        firstColumn = "Empresa"
        secondColumn = 'Instituicao'
    else:
        firstColumn = 'Instituicao'
        secondColumn = "Empresa"

    counter = data.groupby([firstColumn, secondColumn]).size().reset_index(name='Count')
    values = counter[firstColumn].unique()

    df_new = counter.groupby([firstColumn, secondColumn]).sum()

    counts = counter.groupby([firstColumn]).sum()
    areas_values = counts['Count'].nlargest(50)
    if 'valueuniversityorcompany' in request.POST and request.POST['universityorcompany'] == context["universidadeXempresa"]["ChoosedEntity"]:
        choosedValue = request.POST['valueuniversityorcompany']
    else:
        choosedValue = areas_values.index[0]

    dict_values = {}
    finalResult = {}
    area_frame = df_new['Count'][choosedValue]
    area_frame = area_frame.sort_values(ascending=False)
    area_frame = area_frame.nlargest(total)
    areas = area_frame.index.values.tolist()
    numbers = area_frame.values.tolist()
    finalResult["Labels"] = areas
    finalResult["Data"] = numbers
    finalResult["Label"] = "Total"
    finalResult["Values"] = list(values)
    finalResult["ChoosedValue"] = choosedValue
    finalResult["ChoosedEntity"] = choosedEntity
    finalResult["AllValues"] = areas_values.index.tolist()
    finalResult["Total"] = total
    return finalResult

#endregion

#region Profissionais vs Empresa( Genero X Area , ...)
def graphs_profissionais_vs_empresa(request):

    generoXarea = graph_genero_vs_area(request)

    ageXarea = graph_age_vs_area()

    generoXsalario = graph_genero_vs_salario(request)

    context["generoXarea"] = generoXarea
    context["ageXarea"] = ageXarea
    context["generoXsalario"] = generoXsalario

    return render(request, 'metrics/graphs_profissionais_vs_empresa.html', context)

def graph_genero_vs_salario(request):
    finalResult = {}
    if 'Area' in data and 'Genero' in data and 'Salario' in data:
        counter = data.groupby(['Area', 'Genero', 'Salario']).size().reset_index(name='Count')
        gender_counts = counter.groupby(['Area', 'Genero']).sum()
        aggregate_gender_age = data.groupby(['Area', 'Genero']).agg({'Area': 'first', 'Salario': 'sum'})
        counts = counter.groupby(['Area']).sum()
        total = 0
        if 'qtygendersalario' in request.POST:
            total = int(request.POST['qtygendersalario'])
        elif context["generoXsalario"] is None:
            total = 10
        else:
            total = context["generoXsalario"]["Total"]
        areas_values = counts['Count'].nlargest(total)

        list_areas = []
        dict_values = {}
        indexes = gender_counts['Count'].index.levels[1]

        for index, value in areas_values.items():
            list_areas.append(index)
            area_frame = gender_counts['Count'][index]
            for gender in indexes:
                gender_value = 0
                if gender in area_frame.index.values:
                    age_total = aggregate_gender_age['Salario'][index][gender]
                    gender_total = area_frame[gender]
                    gender_value = age_total / gender_total
                if gender not in dict_values:
                    dict_values[gender] = []
                dict_values[gender].append(gender_value)
        finalResult["Areas"] = list_areas
        finalResult["Data"] = list(dict_values.items())
        finalResult["Total"] = total

    return finalResult

def graph_genero_vs_area(request):
    counter = data.groupby(['Area', 'Genero']).size().reset_index(name='Count')
    df_new = counter.groupby(['Area', 'Genero']).sum()

    counts = counter.groupby(['Area']).sum()
    total = 0
    if 'qtygenderarea' in request.POST:
        total = int(request.POST['qtygenderarea'])
    elif context["generoXarea"] is None:
        total = 10
    else:
        total = context["generoXarea"]["Total"]
    areas_values = counts['Count'].nlargest(total)

    list_areas = []
    dict_values = {}
    finalResult = {}
    indexes = df_new['Count'].index.levels[1]

    for index, value in areas_values.items():
        list_areas.append(index)
        area_frame = df_new['Count'][index]
        for gender in indexes:
            gender_value = 0
            if gender in area_frame.index.values:
                gender_value = area_frame[gender]
            if gender not in dict_values:
                dict_values[gender] = []
            dict_values[gender].append(gender_value)
    finalResult["Areas"] = list_areas
    finalResult["Data"] = list(dict_values.items())
    finalResult["Total"] = total
    return finalResult

def graph_age_vs_area():
    counter = data.groupby(['Area', 'Genero', 'Idade']).size().reset_index(name='Count')
    gender_counts = counter.groupby(['Area', 'Genero']).sum()
    aggregate_gender_age = data.groupby(['Area', 'Genero']).agg({'Area': 'first', 'Idade': 'sum'})
    counts = counter.groupby(['Area']).sum()
    areas_values = counts['Count'].nlargest(10)

    list_areas = []
    dict_values = {}
    finalResult = {}
    indexes = gender_counts['Count'].index.levels[1]

    for index, value in areas_values.items():
        list_areas.append(index)
        area_frame = gender_counts['Count'][index]
        for gender in indexes:
            gender_value = 0
            if gender in area_frame.index.values:
                age_total = aggregate_gender_age['Idade'][index][gender]
                gender_total = area_frame[gender]
                gender_value = age_total / gender_total
            if gender not in dict_values:
                dict_values[gender] = []
            dict_values[gender].append(gender_value)
    finalResult["Areas"] = list_areas
    finalResult["Data"] = list(dict_values.items())

    return finalResult

#endregion

#region Profissionais vs Universidade ( Genero X Curso , Genero X Universidade)
def graphs_profissionais_vs_universidade(request):
    generoXcurso = graph_genero_vs_course(request)

    generoXuniversidade = graph_genero_vs_universidade(request)

    context["generoXcurso"] = generoXcurso
    context["generoXuniversidade"] = generoXuniversidade

    return render(request, 'metrics/graphs_profissionais_vs_universidade.html', context)

def graph_genero_vs_course(request):
    finalResult = {}
    if 'Curso' in data and 'Genero' in data:
        data.loc[data['Curso'].str.contains("SISTEMA"), "Curso"] = "SISTEMAS"
        data.loc[data['Curso'].str.contains("ENGENHARIA"), "Curso"] = "ENGENHARIA"
        data.loc[data['Curso'].str.contains("COMPUTACAO"), "Curso"] = "COMPUTACAO"
        data.loc[(data['Curso'] != "SISTEMAS") & (data['Curso'] != "ENGENHARIA") & (data['Curso'] != "COMPUTACAO"), "Curso"] = "OUTROS CURSOS DE TI"

        course = ""
        if 'course' in request.POST:
            course = request.POST['course']
        elif context["generoXcurso"] is None:
            course = "COMPUTACAO"
        else:
            course = context["generoXcurso"]["Course"]

        counter = data.groupby(['Curso', 'Genero']).size().reset_index(name='Count')
        df_new = counter.groupby(['Curso','Genero']).sum()
        courseValue = df_new['Count'][course]
        finalResult["Labels"] = courseValue.index.values.tolist()
        finalResult["Data"] = courseValue.values.tolist()
        finalResult["Course"] = course
    return finalResult

def graph_genero_vs_universidade(request):
    finalResult = {}
    if "Instituicao" in data and 'Genero' in data and 'Estado_Universidade' in data:
        counter = data.groupby(['Instituicao', 'Genero', "Estado_Universidade"]).size().reset_index(name='Count')
        states = counter.Estado_Universidade.unique()
        state = "Todos"
        if 'states' in request.POST:
            state = request.POST['states']
        elif context["generoXuniversidade"] is not None:
            state = context["generoXuniversidade"]["State"]

        if state != "Todos":
            counter = counter[counter.Estado_Universidade == state]

        total = 10
        if 'qtygenderuniversidade' in request.POST:
            total = int(request.POST['qtygenderuniversidade'])
        elif context["generoXuniversidade"] is not None:
            total = context["generoXuniversidade"]["Total"]

        df_new = counter.groupby(['Instituicao', 'Genero']).sum()
        counts = counter.groupby(['Instituicao']).sum()
        areas_values = counts['Count'].nlargest(total)

        list_areas = []
        dict_values = {}
        indexes = df_new['Count'].index.levels[1]

        for index, value in areas_values.items():
            list_areas.append(index)
            area_frame = df_new['Count'][index]
            for gender in indexes:
                gender_value = 0
                if gender in area_frame.index.values:
                    gender_value = area_frame[gender]
                if gender not in dict_values:
                    dict_values[gender] = []
                dict_values[gender].append(gender_value)
        finalResult["Instituicoes"] = list_areas
        finalResult["Data"] = list(dict_values.items())
        finalResult["States"] = list(states)
        finalResult["State"] = state
        finalResult["Total"] = total
    return finalResult
#endregion