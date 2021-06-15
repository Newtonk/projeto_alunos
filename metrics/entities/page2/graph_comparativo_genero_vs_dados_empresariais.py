from metrics.utils import *

class GeneroDadosComparativosEmpresariais():
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
        states = []
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            states = data.Estado_Empresa.dropna().unique()
            selectedState = get_value_string("State", "statesLaborMarketComparation", "Todos", request, "generoXmercadodetrabalhoCompare", context)
        if selectedState != "Todos":
            data = data[data.Estado_Empresa == selectedState]
        return states, selectedState, data

    @staticmethod
    def campo_genero(data, request, context):
        genders = data.Genero.dropna().unique()
        gender = get_value_string("Gender", 'genderLaborMarketComparation', genders[0], request, "generoXmercadodetrabalhoCompare", context)
        return genders, gender

    @staticmethod
    def campo_total(request, context):
        total = get_value_int("Total", 'qtygenderLaborMarketComparation', 10, request, "generoXmercadodetrabalhoCompare", context)
        return total

    @staticmethod
    def campo_area(data, request, context):
        areas = []
        selectedArea = "Todos"
        if checa_valor("Area", data):
            areas = data.Area.dropna().unique()
            selectedArea = get_value_string("Area", "areaLaborMarketComparation", "Todos", request, "generoXmercadodetrabalhoCompare", context)
            if selectedArea not in data.Area.values and selectedArea != "Todos":
                selectedArea = "Todos"
        if selectedArea != "Todos":
            data = data[data.Area == selectedArea]

        return areas, selectedArea, data

    @staticmethod
    def campo_entidade_comparacao(request, context):
        selectedEntity = get_value_string("Entity", "entitygenderLaborMarketComparation", "Empresa", request, "generoXmercadodetrabalhoCompare", context)

        return selectedEntity

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        selectedEntity = GeneroDadosComparativosEmpresariais.campo_entidade_comparacao(request, context)
        ufs = []
        areas = []
        noInfo = False
        if selectedEntity == "Empresa":
            generos, genero = GeneroDadosComparativosEmpresariais.campo_genero(data, request, context)
            ufs, uf, newData = GeneroDadosComparativosEmpresariais.campo_uf_empresa(data, request, context)
            areas, area, newData = GeneroDadosComparativosEmpresariais.campo_area(newData, request, context)
            total = GeneroDadosComparativosEmpresariais.campo_total(request, context)
        else:
            generos, genero = GeneroDadosComparativosEmpresariais.campo_genero(data, request, context)
            uf = "Todos"
            area = "Todos"
            total = GeneroDadosComparativosEmpresariais.campo_total(request, context)

        if selectedEntity in newData:
            complementData = newData.groupby([selectedEntity, 'Genero']).sum()
            newData = complementData.groupby([selectedEntity]).sum()

            newData = newData['Count'].nlargest(total)
        else:
            newData = []
            complementData = []
            noInfo = True

        return ufs, uf, areas, area, generos, genero, total, selectedEntity, complementData, newData, noInfo

