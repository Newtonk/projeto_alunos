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
        return dashboard_profissionais(request)

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

def graph_gender_vs_course():
    #s = data.melt(('Curso', 'Genero')).groupby(['Curso', 'Genero']).size()


    data.loc[data['Curso'].str.contains("SISTEMA"), "Curso"] = "SISTEMAS"
    data.loc[data['Curso'].str.contains("ENGENHARIA"), "Curso"] = "ENGENHARIA"
    data.loc[data['Curso'].str.contains("COMPUTACAO"), "Curso"] = "COMPUTACAO"
    counter = data.groupby(['Curso', 'Genero']).size().reset_index(name='Count')
    df_new = counter.groupby(['Genero','Curso']).sum()
    courses = []
    listResults = []
    genderValues = {}
    colors = [ "green" , "blue" , "black"]
    i = 0
    for firstIndex, firstValue in df_new.items():
        lastLabel = ""
        for secondIndex, genderValue in firstValue.items():
            if secondIndex[0] not in genderValues:
                genderValues[secondIndex[0]] = []
            genderValues[secondIndex[0]].append(genderValue)
            if secondIndex[1] not in courses:
                courses.append(secondIndex[1])
        for key in genderValues:
            result = {}
            result["Label"] = key
            result["Values"] = genderValues[key]
            result["Color"] = colors[i]
            listResults.append(result)
            i += 1
    return listResults, courses

def dashboard_profissionais(request):
    listResults, courses = graph_gender_vs_course()


    context = {
        "listResults" : listResults,
        "courses" : courses
    }



    return render(request, 'metrics/dashboard_profissionais.html',context)