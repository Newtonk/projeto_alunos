from metrics.utils import *

class ClasseDados:
    @staticmethod
    def validacao_colunas(data):
        if checa_valor("Classe", data):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Classe', 'Area', "Curso", "Empresa", "Universidade", "Estado_Empresa", "Estado_Universidade", "Genero"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Empresa", data):
            selectedState = get_multiple_value_string("CompanyState", "statesClassXLaborMarket", "Todos", request, contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Empresa")

        dictValues["CompanyState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_empresa(dictValues, data, request, contextName):
        selectedCompany = ["Todos"]
        if checa_valor("Empresa", data):
            selectedCompany = get_multiple_value_string("Company", "companyClassXLaborMarket", "Todos", request, contextName)
            data, selectedCompany = separate_values_into_list(selectedCompany, data, "Empresa")

        dictValues["Company"] = selectedCompany
        return dictValues, data

    @staticmethod
    def campo_area(dictValues, data, request, contextName):
        selectedArea = ["Todos"]
        if checa_valor("Area", data):
            selectedArea = get_multiple_value_string("Area", "areaClassXLaborMarket", "Todos", request, contextName)
            data, selectedArea = separate_values_into_list(selectedArea, data, "Area")

        dictValues["Area"] = selectedArea
        return dictValues, data

    @staticmethod
    def campo_genero(dictValues, data, request, contextName):
        selectedGender = ["Todos"]
        if checa_valor("Genero", data):
            selectedGender = get_multiple_value_string("Gender", "genderXLaborMarket", "Todos", request,
                                                      contextName)
            data, selectedGender = separate_values_into_list(selectedGender, data, "Genero")

        dictValues["Gender"] = selectedGender
        return dictValues, data

    @staticmethod
    def campo_uf_universidade(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Universidade", data):
            selectedState = get_multiple_value_string("UniversityState", "statesUniClassXLaborMarket", "Todos", request, contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Universidade")

        dictValues["UniversityState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_universidade(dictValues, data, request, contextName):
        selectedUniversity = ["Todos"]
        if checa_valor("Universidade", data):
            selectedUniversity = get_multiple_value_string("University", "universityClassXLaborMarket", "Todos", request, contextName)
            data, selectedUniversity = separate_values_into_list(selectedUniversity, data, "Universidade")

        dictValues["University"] = selectedUniversity
        return dictValues, data

    @staticmethod
    def campo_curso(dictValues, data, request, contextName):
        selectedCurso = ["Todos"]
        if checa_valor("Curso", data):
            selectedCurso = get_multiple_value_string("Course", "courseClassXLaborMarket", "Todos", request, contextName)
            data, selectedCurso = separate_values_into_list(selectedCurso, data, "Curso")

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = None
        noInfo = False
        dictValues = {}
        contextName = context["classeXmercadodetrabalho"]

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa", contextName)
        dictValues, newData = ClasseDados.campo_uf_empresa(dictValues, data, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade", contextName)
        dictValues, newData = ClasseDados.campo_uf_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa", contextName)
        dictValues, newData = ClasseDados.campo_empresa(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Universidade", contextName)
        dictValues, newData = ClasseDados.campo_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area", contextName)
        dictValues, newData = ClasseDados.campo_area(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso", contextName)
        dictValues, newData = ClasseDados.campo_curso(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Genders", "Genero", contextName)
        dictValues, newData = ClasseDados.campo_genero(dictValues, newData, request, contextName)

        if newData.items() == 0:
            noInfo = True

        colunas = pegue_todas_colunas(['Classe'], data)
        newData = newData.groupby(colunas, dropna=True).sum()
        newData = newData['Count']
        return dictValues, newData, noInfo

