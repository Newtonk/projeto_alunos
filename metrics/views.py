from io import BytesIO

from django.contrib.auth import logout
from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from .entities.page1.graph_comparativo_class_vs_dados_academicos import *
from .entities.page1.graph_class_vs_dados_academicos import *
from .entities.page1.graph_comparativo_genero_vs_dados_academicos import *
from .entities.page1.graph_genero_vs_dados_academicos import *
from .entities.page2.graph_genero_vs_dados_empresariais import *
from .entities.page2.graph_comparativo_genero_vs_dados_empresariais import *
from .entities.page2.graph_class_vs_dados_empresariais import *


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

        pre_validations()
        return graphs_profissionais_vs_universidade(request)


    return render(request, 'metrics/home.html', contextHome)

def pre_validations():
    if check_minium_values(["Curso"], data):
        data.loc[data['Curso'].str.contains("SISTEMA", na=False), "Curso"] = "SISTEMAS"
        data.loc[data['Curso'].str.contains("ENGENHARIA", na=False), "Curso"] = "ENGENHARIA"
        data.loc[data['Curso'].str.contains("COMPUTACAO", na=False), "Curso"] = "COMPUTACAO"
        data.loc[(data['Curso'] != "SISTEMAS") & (data['Curso'] != "ENGENHARIA") & (data['Curso'] != "COMPUTACAO"), "Curso"] = "OUTROS CURSOS DE TI"

def read_file_success(filename, fileExtension):
    global data
    try:
        if fileExtension == "csv":
            myFile = pd.read_csv(BytesIO(filename.read()))
        elif fileExtension == "xlsx":
            myFile = pd.read_excel(BytesIO(filename.read()))

        data = pd.DataFrame(data=myFile, index=None)
    except:
        return False
    return True

def logoutUser(request):
	logout(request)
	return redirect('home')

def update_graph(request):
    graph_name = request.POST["graph_name"]

    if graph_name == "generoXcurso":
        context["generoXcurso"] = graph_genero_vs_course(request)
    elif graph_name == "generoXcursoCompare":
        context["generoXcursoCompare"] = graph_genero_vs_course_comparation(request)
    elif graph_name == "classeXcurso":
        context["classeXcurso"] = graph_social_class_vs_course(request)
    elif graph_name == "classeXcursoCompare":
        context["classeXcursoCompare"] = graph_social_class_vs_course_comparation(request)
    elif graph_name == "generoXmercadodetrabalho":
        context["generoXmercadodetrabalho"] = graph_genero_vs_mercado_trabalho(request)
    elif graph_name == "generoXmercadodetrabalhoCompare":
        context["generoXmercadodetrabalhoCompare"] = graph_genero_vs_mercado_trabalho_comparativo(request)
    elif graph_name == "classeXmercadodetrabalho":
        context["classeXmercadodetrabalho"] = graph_classe_vs_mercado_trabalho(request)
    elif graph_name == "ageXarea":
        context["ageXarea"] = graph_age_vs_area(request)
    elif graph_name == "generoXarea":
        context["generoXarea"] = graph_genero_vs_area(request)
    elif graph_name == "generoXsalario":
        context["generoXsalario"] = graph_genero_vs_salario(request)
    elif graph_name == "areaXcurso":
        context["areaXcurso"] = graph_area_vs_curso(request)
    elif graph_name == "universidadeXempresa":
        context["universidadeXempresa"] = graph_university_vs_company(request)

    return JsonResponse(context, safe=False)

#region Universidade vs Empresa ( Area X Curso , ...)
def graphs_universidade_vs_empresa(request):
    context["areaXcurso"] = None
    context["universidadeXempresa"] = None

    areaXcurso = graph_area_vs_curso(request)

    universidadeXempresa = graph_university_vs_company(request)

    context["areaXcurso"] = areaXcurso

    context["universidadeXempresa"] = universidadeXempresa

    return render(request, 'metrics/page3/graphs_universidade_vs_empresa.html', context)

def check_minium_values(listValues, data):

    for value in listValues:
        if value not in data or data[value].count() == 0:
            return False
    return True

def graph_area_vs_curso(request):
    finalResult = {}
    if check_minium_values(["Curso" , "Area"], data):
        counter = data.groupby(['Curso', 'Area']).size().reset_index(name='Count')
        courses = counter.Curso.unique()
        df_new = counter.groupby(['Curso', 'Area']).sum()
        df_new = df_new.sort_values(by=['Count'], ascending=False)

        course = courses[0]
        if 'course' in request.POST:
            course = request.POST['course']
        elif context["areaXcurso"] is not None:
            course = context["areaXcurso"]["Course"]

        total = 10
        if 'qtyareacourse' in request.POST:
            total = int(request.POST['qtyareacourse'])
        elif context["areaXcurso"] is not None:
            total = context["areaXcurso"]["Total"]

        courseValue = df_new['Count'][course].nlargest(total)
        finalResult["Labels"] = courseValue.index.values.tolist()
        finalResult["Data"] = courseValue.values.tolist()
        finalResult["Course"] = course
        finalResult["Courses"] = list(courses)
        finalResult["Total"] = total
    return finalResult

def graph_university_vs_company(request):
    finalResult = {}
    if check_minium_values(["Empresa", "Instituicao"], data):
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

        if context["universidadeXempresa"] is not None and context["universidadeXempresa"]["ChoosedEntity"] is not None:
            lastChoosedEntity = context["universidadeXempresa"]["ChoosedEntity"]
        else:
            lastChoosedEntity = "Empresas"

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
        finalResult["LastChoosedEntity"] = lastChoosedEntity
        finalResult["AllValues"] = areas_values.index.tolist()
        finalResult["Total"] = total
    return finalResult

#endregion

#region Profissionais vs Empresa( Genero X Area , ...)
def graphs_profissionais_vs_empresa(request):
    context["generoXmercadodetrabalho"] = None
    context["generoXmercadodetrabalhoCompare"] = None
    context["classeXmercadodetrabalho"] = None
    context["generoXarea"] = None
    context["ageXarea"] = None
    context["generoXsalario"] = None

    generoXmercadodetrabalho = graph_genero_vs_mercado_trabalho(request)

    generoXmercadodetrabalhoCompare = graph_genero_vs_mercado_trabalho_comparativo(request)

    classeXmercadodetrabalho = graph_classe_vs_mercado_trabalho(request)

    generoXarea = graph_genero_vs_area(request)

    ageXarea = graph_age_vs_area(request)

    generoXsalario = graph_genero_vs_salario(request)

    context["generoXmercadodetrabalho"] = generoXmercadodetrabalho
    context["generoXmercadodetrabalhoCompare"] = generoXmercadodetrabalhoCompare
    context["classeXmercadodetrabalho"] = classeXmercadodetrabalho
    context["generoXarea"] = generoXarea
    context["ageXarea"] = ageXarea
    context["generoXsalario"] = generoXsalario

    return render(request, 'metrics/page2/graphs_profissionais_vs_empresa.html', context)

def graph_genero_vs_mercado_trabalho(request):
    finalResult = {}
    if GeneroDadosEmpresariais.validacao_colunas(data):
        workingData = data
        newData = GeneroDadosEmpresariais.unifica_colunas(workingData)
        states, state, companies, company, areas, area, areaValue, noInfo = GeneroDadosEmpresariais.valida_dados_enviados(newData, request, context)

        listTotal = []
        indexes = []
        if not noInfo:
            if len(areaValue.index.names) > 1:
                position = areaValue.index.names.index("Genero")
                listLabels = areaValue.index.levels[position].values.tolist()
                indexes = areaValue.index.levels[position]
            elif len(areaValue.index.names) == 1:
                listLabels = areaValue.index.values.tolist()
                indexes = areaValue.index

            for index in indexes:
                if index in areaValue:
                    sum = 0
                    if len(areaValue.index.names) > 1:
                        sum = int(areaValue[index].values.sum())
                    elif len(areaValue.index.names) == 1:
                        sum = int(areaValue[index].sum())
                    listTotal.append(sum)
                else:
                    listLabels.remove(index)
        finalResult["Labels"] = listLabels
        finalResult["Data"] = listTotal
        finalResult["State"] = state
        finalResult["States"] = list(states)
        finalResult["Empresa"] = company
        finalResult["Empresas"] = list(companies)
        finalResult["Area"] = area
        finalResult["Areas"] = list(areas)
    return finalResult

def graph_genero_vs_mercado_trabalho_comparativo(request):
    finalResult = {}
    if GeneroDadosComparativosEmpresariais.validacao_colunas(data):
        workingData = data
        newData = GeneroDadosComparativosEmpresariais.unifica_colunas(workingData)
        states, state, areas, area, genders, gender, total, entity, complementData, finalData, noInfo = GeneroDadosComparativosEmpresariais.valida_dados_enviados(
            newData, request, context)
        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Area"] = index
                area_frame = complementData['Count'][index]
                total_people = area_frame.sum()
                if gender in area_frame:
                    result["GenderValue"] = (int(area_frame[gender]) * 100) / total_people
                    all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["GenderValue"], reverse=True)

                list_entities = list(o["Area"] for o in all_values)
                list_values = list(o["GenderValue"] for o in all_values)

        finalResult["Entities"] = list_entities
        finalResult["Entity"] = entity
        finalResult["Data"] = list_values
        finalResult["States"] = list(states)
        finalResult["State"] = state
        finalResult["Total"] = total
        finalResult["Gender"] = gender
        finalResult["Genders"] = list(genders)
        finalResult["Area"] = area
        finalResult["Areas"] = list(areas)
    return finalResult

def graph_classe_vs_mercado_trabalho(request):
    finalResult = {}
    if ClasseDadosEmpresariais.validacao_colunas(data):
        workingData = data
        newData = ClasseDadosEmpresariais.unifica_colunas(workingData)
        states, state, companies, company, areas, area, areaValue, noInfo = ClasseDadosEmpresariais.valida_dados_enviados(newData, request, context)

        listTotal = []
        indexes = []
        if not noInfo:
            if len(areaValue.index.names) > 1:
                position = areaValue.index.names.index("Classe")
                listLabels = areaValue.index.levels[position].values.tolist()
                indexes = areaValue.index.levels[position]
            elif len(areaValue.index.names) == 1:
                listLabels = areaValue.index.values.tolist()
                indexes = areaValue.index

            listLabels = [x for x in listLabels if str(x) != 'nan']
            if len(listLabels) > 0:
                for index in indexes:
                    if index in areaValue:
                        sum = 0
                        if len(areaValue.index.names) > 1:
                            sum = int(areaValue[index].values.sum())
                        elif len(areaValue.index.names) == 1:
                            sum = int(areaValue[index].sum())
                        listTotal.append(sum)
                    elif index in listLabels:
                        listLabels.remove(index)
        finalResult["Labels"] = listLabels
        finalResult["Data"] = listTotal
        finalResult["State"] = state
        finalResult["States"] = list(states)
        finalResult["Empresa"] = company
        finalResult["Empresas"] = list(companies)
        finalResult["Area"] = area
        finalResult["Areas"] = list(areas)
    return finalResult


def graph_genero_vs_salario(request):
    finalResult = {}
    if check_minium_values(["Area" , "Genero", "Salario"], data):
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
    finalResult = {}
    if check_minium_values(["Area", "Genero"], data):
        counter = data.groupby(['Area', 'Genero']).size().reset_index(name='Count')
        df_new = counter.groupby(['Area', 'Genero']).sum()

        counts = counter.groupby(['Area']).sum()
        total = 10
        if 'qtygenderarea' in request.POST:
            total = int(request.POST['qtygenderarea'])
        elif context["generoXarea"] is not None:
            total = context["generoXarea"]["Total"]
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
                dict_values[gender].append(int(gender_value))
        finalResult["Areas"] = list_areas
        finalResult["Data"] = list(dict_values.items())
        finalResult["Total"] = total
    return finalResult

def graph_age_vs_area(request):
    finalResult = {}
    if check_minium_values(["Area", "Genero" , "Idade"], data):
        counter = data.groupby(['Area', 'Genero', 'Idade']).size().reset_index(name='Count')
        gender_counts = counter.groupby(['Area', 'Genero']).sum()
        aggregate_gender_age = data.groupby(['Area', 'Genero']).agg({'Area': 'first', 'Idade': 'sum'})
        counts = counter.groupby(['Area']).sum()

        total = 10
        if 'qtyagearea' in request.POST:
            total = int(request.POST['qtyagearea'])
        elif context["ageXarea"] is not None:
            total = context["ageXarea"]["Total"]
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
                    age_total = aggregate_gender_age['Idade'][index][gender]
                    gender_total = area_frame[gender]
                    gender_value = age_total / gender_total
                if gender not in dict_values:
                    dict_values[gender] = []
                dict_values[gender].append(gender_value)
        finalResult["Areas"] = list_areas
        finalResult["Data"] = list(dict_values.items())
        finalResult["Total"] = total
    return finalResult

#endregion

#region Profissionais vs Universidade ( Genero X Curso , Genero X Universidade)
def graphs_profissionais_vs_universidade(request):
    context["generoXcurso"] = None
    context["generoXcursoCompare"] = None
    context["classeXcurso"] = None
    context["classeXcursoCompare"] = None

    generoXcurso = graph_genero_vs_course(request)

    generoXcursoCompare = graph_genero_vs_course_comparation(request)

    classeXcurso = graph_social_class_vs_course(request)

    classeXcursoCompare = graph_social_class_vs_course_comparation(request)

    context["generoXcurso"] = generoXcurso
    context["generoXcursoCompare"] = generoXcursoCompare
    context["classeXcurso"] = classeXcurso
    context["classeXcursoCompare"] = classeXcursoCompare

    return render(request, 'metrics/page1/graphs_profissionais_vs_universidade.html', context)


def graph_genero_vs_course(request):
    finalResult = {}
    if GeneroDadosAcademicos.validacao_colunas(data):
        workingData = data
        newData = GeneroDadosAcademicos.unifica_colunas(workingData)
        states, state, universities, university, courses, course, courseValue = GeneroDadosAcademicos.valida_dados_enviados(newData, request, context)

        listTotal = []
        indexes = []
        if len(courseValue.index.names) > 1:
            position = courseValue.index.names.index("Genero")
            listLabels = courseValue.index.levels[position].values.tolist()
            indexes = courseValue.index.levels[position]
        elif len(courseValue.index.names) == 1:
            listLabels = courseValue.index.values.tolist()
            indexes = courseValue.index

        for index in indexes:
            if index in courseValue:
                sum = 0
                if len(courseValue.index.names) > 1:
                    sum = int(courseValue[index].values.sum())
                elif len(courseValue.index.names) == 1:
                    sum = int(courseValue[index].sum())
                listTotal.append(sum)
            else:
                listLabels.remove(index)
        finalResult["Labels"] = listLabels
        finalResult["Data"] = listTotal
        finalResult["State"] = state
        finalResult["States"] = list(states)
        finalResult["Instituicao"] = university
        finalResult["Instituicoes"] = list(universities)
        finalResult["Course"] = course
        finalResult["Courses"] = list(courses)
    return finalResult

def graph_genero_vs_course_comparation(request):
    finalResult = {}
    if GeneroDadosComparativos.validacao_colunas(data):
        workingData = data
        newData = GeneroDadosComparativos.unifica_colunas(workingData)
        states, state, courses, course, genders, gender, total, entity, complementData, finalData, noInfo = GeneroDadosComparativos.valida_dados_enviados(newData, request, context)
        all_values = []
        list_entities = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Entity"] = index
                area_frame = complementData['Count'][index]
                total_people = area_frame.sum()
                if gender in area_frame:
                    result["GenderValue"] = (int(area_frame[gender]) * 100) / total_people
                    all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["GenderValue"], reverse=True)

                list_entities = list(o["Entity"] for o in all_values)
                list_values = list(o["GenderValue"] for o in all_values)

        finalResult["Instituicoes"] = list_entities
        finalResult["Data"] = list_values
        finalResult["States"] = list(states)
        finalResult["State"] = state
        finalResult["Total"] = total
        finalResult["Gender"] = gender
        finalResult["Genders"] = list(genders)
        finalResult["Course"] = course
        finalResult["Courses"] = list(courses)
        finalResult["Entity"] = entity
    return finalResult

def graph_social_class_vs_course(request):
    finalResult = {}
    if ClasseDadosAcademicos.validacao_colunas(data):
        workingData = data
        newData = ClasseDadosAcademicos.unifica_colunas(workingData)
        states, state, universities, university, courses, course, courseValue = ClasseDadosAcademicos.valida_dados_enviados(newData, request, context)

        listTotal = []
        listLabels = courseValue.index.levels[0].values.tolist()
        for index in courseValue.index.levels[0]:
            if index in courseValue:
                sum = int(courseValue[index].values.sum())
                listTotal.append(sum)
            else:
                listLabels.remove(index)
        finalResult["Labels"] = listLabels
        finalResult["Data"] = listTotal
        finalResult["State"] = state
        finalResult["States"] = list(states)
        finalResult["Instituicao"] = university
        finalResult["Instituicoes"] = list(universities)
        finalResult["Course"] = course
        finalResult["Courses"] = list(courses)
    return finalResult

def graph_social_class_vs_course_comparation(request):
    finalResult = {}
    if ClasseDadosComparativos.validacao_colunas(data):
        workingData = data
        newData = ClasseDadosComparativos.unifica_colunas(workingData)
        states, state, courses, course, classes, selectedClass, total, entity, complementData, finalData, noInfo = ClasseDadosComparativos.valida_dados_enviados(
            newData, request, context)
        all_values = []
        list_areas = []
        list_values = []
        if not noInfo:
            for index, value in finalData.items():
                result = {}
                result["Area"] = index
                area_frame = complementData['Count'][index]
                total_people = area_frame.sum()
                if selectedClass in area_frame:
                    result["ClassValue"] = (int(area_frame[selectedClass]) * 100) / total_people
                    all_values.append(result)
            if len(all_values) > 0:
                all_values.sort(key=lambda x: x["ClassValue"], reverse=True)

                list_areas = list(o["Area"] for o in all_values)
                list_values = list(o["ClassValue"] for o in all_values)

        finalResult["Instituicoes"] = list_areas
        finalResult["Data"] = list_values
        finalResult["States"] = list(states)
        finalResult["State"] = state
        finalResult["Total"] = total
        finalResult["Class"] = selectedClass
        finalResult["Classes"] = list(classes)
        finalResult["Course"] = course
        finalResult["Courses"] = list(courses)
        finalResult["Entity"] = entity
    return finalResult

#endregion

def get_all_columns(columns, data):
    existingColumns = []
    for column in columns:
        if check_minium_values([column],data):
            existingColumns.append(column)
    return existingColumns

def get_value_string(objName , key, defaultValue, request, contextName):
    finalValue = defaultValue
    if key in request.POST:
        finalValue = request.POST[key]
    elif context[contextName] is not None:
        finalValue = context[contextName][objName]
    return finalValue

def get_value_int(objName , key, defaultValue, request, contextName):
    finalValue = defaultValue
    if key in request.POST:
        finalValue = int(request.POST[key])
    elif context[contextName] is not None:
        finalValue = context[contextName][objName]
    return finalValue