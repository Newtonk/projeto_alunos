import base64
from io import BytesIO, StringIO

from PIL import Image
from django.shortcuts import render, redirect
import pandas as pd
import openpyxl
# Create your views here.
from openpyxl import Workbook
from openpyxl.chart import Reference, BarChart3D, LineChart, PieChart
from openpyxl_image_loader import SheetImageLoader
import matplotlib.pyplot as plt
from django.core.cache import cache

data = None

def home(request):
    context = {}
    if request.method == 'POST':
        filename = request.FILES['File']

        data = pd.read_csv(BytesIO(filename.read()))

        #s = data.melt(('Curso', 'Genero')).groupby(['Curso' , 'Genero']).size()
        cache.set('data_store', data, timeout=600)
        return dashboard(request)

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

def dashboard(request):
    df = cache.get('data_store')
    return render(request, 'metrics/dashboard.html')