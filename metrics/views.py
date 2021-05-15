import base64
from io import BytesIO, StringIO

from PIL import Image
from django.shortcuts import render, redirect
import pandas as pd
from django.core.cache import cache

data = None

def home(request):
    context = {}
    if request.method == 'POST':
        filename = request.FILES['File']

        read_csv(filename)
        #s = data.melt(('Curso', 'Genero')).groupby(['Curso' , 'Genero']).size()
        #cache.set('data_store', data, timeout=600)
        return graphs_profissionais_vs_universidade(request)

        #ax = s.plot.bar(rot=0)
        #plt.show()
        #cs.add_chart(chart)
        #file.save("newshart.xlsx")
        #image_loader = SheetImageLoader(cs)
        #image = image_loader.get('A3')
        #data = BytesIO(image)
        #Image.save(data, "JPEG")
        #encoded_img_data = base64.b64encode(data.getvalue())

        #context = { "image_chart" : encoded_img_data.decode('utf-8')}
    return render(request, 'metrics/home.html', context)


def read_csv(filename):
    global data

    myFile = pd.read_csv(BytesIO(filename.read()))

    data = pd.DataFrame(data=myFile, index=None)

def graph_genero_vs_course():

    data.loc[data['Curso'].str.contains("SISTEMA"), "Curso"] = "SISTEMAS"
    data.loc[data['Curso'].str.contains("ENGENHARIA"), "Curso"] = "ENGENHARIA"
    data.loc[data['Curso'].str.contains("COMPUTACAO"), "Curso"] = "COMPUTACAO"
    counter = data.groupby(['Curso', 'Genero']).size().reset_index(name='Count')
    df_new = counter.groupby(['Curso','Genero']).sum()
    generos = []
    listResults = []
    cursosValues = {}
    finalResult = {}
    colors = ["green", "blue", "black"]
    i = 0
    for firstIndex, firstValue in df_new.items():
        for secondIndex, genderValue in firstValue.items():
            if secondIndex[0] not in cursosValues:
                cursosValues[secondIndex[0]] = []
            cursosValues[secondIndex[0]].append(genderValue)
            if secondIndex[1] not in generos:
                generos.append(secondIndex[1])
        for key in cursosValues:
            result = {}
            result["Label"] = key
            result["Valores"] = cursosValues[key]
            result["Cores"] = colors
            result["Id"] = str(i)
            listResults.append(result)
            i += 1
    finalResult["Generos"] = generos
    finalResult["Data"] = listResults
    return finalResult

def graph_genero_vs_universidade():
    counter = data.groupby(['Instituicao', 'Genero']).size().reset_index(name='Count')
    df_new = counter.groupby(['Instituicao', 'Genero']).sum()

    counts = counter.groupby(['Instituicao']).sum()
    areas_values = counts['Count'].nlargest(10)

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
    finalResult["Instituicoes"] = list_areas
    finalResult["Data"] = list(dict_values.items())

    return finalResult

def graph_genero_vs_area():
    counter = data.groupby(['Area', 'Genero']).size().reset_index(name='Count')
    df_new = counter.groupby(['Area', 'Genero']).sum()

    counts = counter.groupby(['Area']).sum()
    areas_values = counts['Count'].nlargest(10)

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

    return finalResult

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

def graphs_universidade_vs_empresa(request):
    areaXcurso = graph_area_vs_curso()

    context = {
        "areaXcurso": areaXcurso
    }

    return render(request, 'metrics/graphs_universidade_vs_empresa.html', context)
def graphs_profissionais_vs_empresa(request):

    generoXarea = graph_genero_vs_area()

    context = {
        "generoXarea": generoXarea
    }

    return render(request, 'metrics/graphs_profissionais_vs_empresa.html', context)

def graphs_profissionais_vs_universidade(request):
    generoXcurso = graph_genero_vs_course()

    generoXuniversidade = graph_genero_vs_universidade()

    context = {
        "generoXcurso": generoXcurso,
        "generoXuniversidade": generoXuniversidade
    }



    return render(request, 'metrics/graphs_profissionais_vs_universidade.html',context)