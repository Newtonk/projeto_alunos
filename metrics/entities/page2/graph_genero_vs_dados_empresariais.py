from metrics.utils import *

class GeneroDadosEmpresariais:
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Area', 'Empresa', "Genero", "Estado_Empresa"], data)
        if "Genero" in colunas and ("Area" in colunas or "Empresa" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Genero', 'Area', "Empresa", "Estado_Empresa"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_uf_empresa(data, request, context):
        ufs = []
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            ufs = data.Estado_Empresa.dropna().unique()
            selectedState = get_value_string("State", "statesGenderXLaborMarket", "Todos", request, "generoXmercadodetrabalho", context)
        if selectedState != "Todos":
            data = data[data.Estado_Empresa == selectedState]
        return ufs, selectedState, data

    @staticmethod
    def campo_empresa(data, request, context):
        companies = []
        selectedCompany = "Todos"
        if checa_valor("Empresa", data):
            companies = data.Empresa.dropna().unique()
            selectedCompany = get_value_string("Empresa", "companyGenderXLaborMarket", "Todos", request, "generoXmercadodetrabalho", context)
            if "statesGenderXLaborMarket" in request.POST and request.POST["statesGenderXLaborMarket"] != context["generoXmercadodetrabalho"]["State"]:
                selectedCompany = "Todos"
        if selectedCompany != "Todos":
            data = data[data.Empresa == selectedCompany]
        return companies, selectedCompany, data

    @staticmethod
    def campo_area(data, request, context):
        areas = []
        selectedArea = "Todos"
        if checa_valor("Area", data):
            areas = data.Area.dropna().unique()
            selectedArea = get_value_string("Area", "areaGenderXLaborMarket", "Todos", request, "generoXmercadodetrabalho", context)
            if selectedArea not in data.Area.values and selectedArea != "Todos":
                selectedArea = areas[0]
        if selectedArea != "Todos":
            data = data[data.Area == selectedArea]

        return areas, selectedArea, data

    @staticmethod
    def pega_valores_do_campo(campo, data):
        valores = []
        if checa_valor(campo, data):
            valores = data[campo].dropna().unique()
        return valores
    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = None
        noInfo = False
        ufs, uf, newData = GeneroDadosEmpresariais.campo_uf_empresa(data, request, context)
        companies, company, newData = GeneroDadosEmpresariais.campo_empresa(newData, request, context)
        areas, area, newData = GeneroDadosEmpresariais.campo_area(newData, request, context)

        if newData.items() == 0:
            noInfo = True

        colunas = pegue_todas_colunas(['Area', 'Genero', "Empresa", "Estado_Empresa"], data)
        if checa_valor("Area", data):
            if area == "Todos":
                colunas.remove("Area")
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count']
            else:
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count'][area]
        elif checa_valor("Empresa", data):
            if company == "Todos":
                colunas.remove("Empresa")
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count']
            else:
                colunas.remove("Empresa")
                colunas.insert(0, "Empresa")
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count'][company]
        return ufs, uf, companies, company, areas, area, newData ,  noInfo

