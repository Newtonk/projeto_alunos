from metrics.utils import *

class ClasseDadosComparativosEmpresariais():
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Area', 'Empresa', "Classe", "Estado_Empresa"], data)
        if "Classe" in colunas and ("Area" in colunas or "Empresa" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Classe', 'Area', "Empresa", "Estado_Empresa"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_uf_empresa(data, request, context):
        states = []
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            states = data.Estado_Empresa.dropna().unique()
            selectedState = get_value_string("State", "statesclassLaborMarketComparation", "Todos", request, "classeXmercadodetrabalhoCompare", context)
        if selectedState != "Todos":
            data = data[data.Estado_Empresa == selectedState]
        return states, selectedState, data

    @staticmethod
    def campo_classe(data, request, context):
        classes = data.Classe.dropna().unique()
        selectedClass = get_value_string("Class", 'classLaborMarketComparation', classes[0], request, "classeXmercadodetrabalhoCompare", context)
        return classes, selectedClass

    @staticmethod
    def campo_total(request, context):
        total = get_value_int("Total", 'qtyclassLaborMarketComparation', 10, request, "classeXmercadodetrabalhoCompare", context)
        return total

    @staticmethod
    def campo_area(data, request, context):
        areas = []
        selectedArea = "Todos"
        if checa_valor("Area", data):
            areas = data.Area.dropna().unique()
            selectedArea = get_value_string("Area", "areaclassLaborMarketComparation", "Todos", request, "classeXmercadodetrabalhoCompare", context)
            if selectedArea not in data.Area.values and selectedArea != "Todos":
                selectedArea = "Todos"
        if selectedArea != "Todos":
            data = data[data.Area == selectedArea]

        return areas, selectedArea, data

    @staticmethod
    def campo_entidade_comparacao(request, context):
        selectedEntity = get_value_string("Entity", "entityclassLaborMarketComparation", "Empresa", request, "classeXmercadodetrabalhoCompare", context)

        return selectedEntity

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        selectedEntity = ClasseDadosComparativosEmpresariais.campo_entidade_comparacao(request, context)
        ufs = []
        areas = []
        noInfo = False
        if selectedEntity == "Empresa":
            classes, selectedClass = ClasseDadosComparativosEmpresariais.campo_classe(data, request, context)
            ufs, uf, newData = ClasseDadosComparativosEmpresariais.campo_uf_empresa(data, request, context)
            areas, area, newData = ClasseDadosComparativosEmpresariais.campo_area(newData, request, context)
            total = ClasseDadosComparativosEmpresariais.campo_total(request, context)
        else:
            classes, selectedClass = ClasseDadosComparativosEmpresariais.campo_classe(data, request, context)
            uf = "Todos"
            area = "Todos"
            total = ClasseDadosComparativosEmpresariais.campo_total(request, context)

        if selectedEntity in newData:
            complementData = newData.groupby([selectedEntity, 'Classe']).sum()
            newData = complementData.groupby([selectedEntity]).sum()

            newData = newData['Count'].nlargest(total)
        else:
            newData = []
            complementData = []
            noInfo = True

        return ufs, uf, areas, area, classes, selectedClass, total, selectedEntity, complementData, newData, noInfo

