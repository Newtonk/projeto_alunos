from metrics.utils import *

class QuantidadeDadosComparativos():
    @staticmethod
    def validacao_colunas(entityValue, data):
        if checa_valor(entityValue, data):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Idade', 'Area', "Curso", "Empresa", "Salario", "Instituicao", "Estado_Empresa", "Estado_Universidade", "Genero", 'Classe'], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_total(request, contextName):
        total = get_value_int("Total", 'qtyQuantityDataComparation', 10, request, contextName)
        return total

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Empresa", data):
            selectedState = get_multiple_value_string("CompanyState", "statesQuantityDataComparation", "Todos", request,
                                                      contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Empresa")
        dictValues["CompanyState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_empresa(dictValues, data, request, contextName):
        selectedCompany = ["Todos"]
        if checa_valor("Empresa", data):
            selectedCompany = get_multiple_value_string("Company", "companyQuantityDataComparation", "Todos", request, contextName)
            data, selectedCompany = separate_values_into_list(selectedCompany, data, "Empresa")

        dictValues["Company"] = selectedCompany
        return dictValues, data

    @staticmethod
    def campo_area(dictValues, data, request, contextName):
        selectedArea = ["Todos"]
        if checa_valor("Area", data):
            selectedArea = get_multiple_value_string("Area", "areaQuantityDataComparation", "Todos", request, contextName)
            data, selectedArea = separate_values_into_list(selectedArea, data, "Area")

        dictValues["Area"] = selectedArea
        return dictValues, data

    @staticmethod
    def campo_uf_universidade(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Universidade", data):
            selectedState = get_multiple_value_string("UniversityState", "statesUniQuantityDataComparation", "Todos", request,
                                             contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Universidade")

        dictValues["UniversityState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_universidade(dictValues, data, request, contextName):
        selectedUniversity = ["Todos"]
        if checa_valor("Instituicao", data):
            selectedUniversity = get_multiple_value_string("University", "universityQuantityDataComparation", "Todos", request,
                                                  contextName)
            data, selectedUniversity = separate_values_into_list(selectedUniversity, data, "Instituicao")

        dictValues["University"] = selectedUniversity
        return dictValues, data

    @staticmethod
    def campo_curso(dictValues, data, request, contextName):
        selectedCurso = ["Todos"]
        if checa_valor("Curso", data):
            selectedCurso = get_multiple_value_string("Course", "courseQuantityDataComparation", "Todos", request,
                                             contextName)
            data, selectedCurso = separate_values_into_list(selectedCurso, data, "Curso")

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def campo_classe(dictValues, data, request, contextName):
        selectedClass = ["Todos"]
        if checa_valor("Classe", data):
            selectedClass = get_multiple_value_string("Class", "classQuantityDataComparation", "Todos", request,
                                              contextName)
            data, selectedClass = separate_values_into_list(selectedClass, data, "Classe")

        dictValues["Class"] = selectedClass

        return dictValues, data

    @staticmethod
    def campo_genero(dictValues, data, request, contextName):
        selectedGender = ["Todos"]
        if checa_valor("Genero", data):
            selectedGender = get_multiple_value_string("Gender", "genderQuantityDataComparation", "Todos", request,
                                             contextName)
            data, selectedGender = separate_values_into_list(selectedGender, data, "Genero")

        dictValues["Gender"] = selectedGender
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(dictValues, request, contextName):
        selectedEntity = get_value_string("Entity", "entityQuantityDataComparation", "Empresa", request, contextName)
        return selectedEntity

    @staticmethod
    def campo_ordenacao(request, contextName):
        order = get_value_string("Order", 'maxMinQuantityLaborMarketComparation', "Max", request, contextName)
        return order

    @staticmethod
    def valida_dados_enviados(data, request, contextName, entityValue):
        newData = data
        dictValues = {}
        noInfo = False

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_uf_empresa(dictValues, data, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_uf_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_empresa(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_area(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_curso(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Genders", "Genero", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_genero(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Classes", "Classe", contextName)
        dictValues, newData = QuantidadeDadosComparativos.campo_classe(dictValues, newData, request, contextName)

        dictValues["Total"] = QuantidadeDadosComparativos.campo_total(request, contextName)

        dictValues["Order"] = QuantidadeDadosComparativos.campo_ordenacao(request, contextName)

        if newData.items() == 0:
            noInfo = True

        if entityValue in newData:
            newData = newData.groupby(entityValue).sum()
            newData = newData['Count'].nlargest(dictValues["Total"])
        else:
            newData = []
            noInfo = True

        return dictValues, newData, noInfo