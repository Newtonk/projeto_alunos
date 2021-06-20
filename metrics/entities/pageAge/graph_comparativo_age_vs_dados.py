from metrics.utils import *

class IdadeDadosComparativos():
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Idade', 'Area', 'Empresa', "Instituicao", "Curso", "Classe", "Estado_Empresa", "Estado_Universidade", "Genero"], data)
        if "Idade" in colunas and ("Area" in colunas or "Empresa" in colunas or "Curso" in colunas or "Instituicao" in colunas or "Genero" in colunas or "Classe" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Idade', 'Area', "Curso", "Empresa", "Instituicao", "Estado_Empresa", "Estado_Universidade", "Genero", 'Classe'], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_total(request, contextName):
        total = get_value_int("Total", 'qtyAgeDataComparation', 10, request, contextName)
        return total

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Empresa", data):
            selectedState = get_multiple_value_string("CompanyState", "statesAgeDataComparation", "Todos", request, contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Empresa")

        dictValues["CompanyState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_empresa(dictValues, data, request, contextName):
        selectedCompany = ["Todos"]
        if checa_valor("Empresa", data):
            selectedCompany = get_multiple_value_string("Company", "companyAgeDataComparation", "Todos", request, contextName)
            data, selectedCompany = separate_values_into_list(selectedCompany, data, "Empresa")

        dictValues["Company"] = selectedCompany
        return dictValues, data

    @staticmethod
    def campo_area(dictValues, data, request, contextName):
        selectedArea = ["Todos"]
        if checa_valor("Area", data):
            selectedArea = get_multiple_value_string("Area", "areaAgeDataComparation", "Todos", request, contextName)
            data, selectedArea = separate_values_into_list(selectedArea, data, "Area")

        dictValues["Area"] = selectedArea
        return dictValues, data

    @staticmethod
    def campo_uf_universidade(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Universidade", data):
            selectedState = get_multiple_value_string("UniversityState", "statesUniAgeDataComparation", "Todos", request,
                                             contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Universidade")

        dictValues["UniversityState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_universidade(dictValues, data, request, contextName):
        selectedUniversity = ["Todos"]
        if checa_valor("Instituicao", data):
            selectedUniversity = get_multiple_value_string("University", "universityAgeDataComparation", "Todos", request,
                                                  contextName)
            data, selectedUniversity = separate_values_into_list(selectedUniversity, data, "Instituicao")

        dictValues["University"] = selectedUniversity
        return dictValues, data

    @staticmethod
    def campo_curso(dictValues, data, request, contextName):
        selectedCurso = ["Todos"]
        if checa_valor("Curso", data):
            selectedCurso = get_multiple_value_string("Course", "courseAgeDataComparation", "Todos", request,
                                             contextName)
            data, selectedCurso = separate_values_into_list(selectedCurso, data, "Curso")

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def campo_classe(dictValues, data, request, contextName):
        selectedClass = ["Todos"]
        if checa_valor("Classe", data):
            selectedClass = get_multiple_value_string("Class", "classAgeDataComparation", "Todos", request,
                                              contextName)
            data, selectedClass = separate_values_into_list(selectedClass, data, "Classe")

        dictValues["Class"] = selectedClass

        return dictValues, data

    @staticmethod
    def campo_genero(dictValues, data, request, contextName):
        selectedGender = ["Todos"]
        if checa_valor("Genero", data):
            selectedGender = get_multiple_value_string("Gender", "genderAgeDataComparation", "Todos", request,
                                             contextName)
            data, selectedGender = separate_values_into_list(selectedGender, data, "Genero")

        dictValues["Gender"] = selectedGender
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(dictValues, request, contextName):
        selectedEntity = get_value_string("Entity", "entityAgeDataComparation", "Empresa", request, contextName)
        dictValues["Entity"] = selectedEntity

        return dictValues

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        dictValues = {}
        noInfo = False
        contextName = context["idadeXdadosCompare"]

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_uf_empresa(dictValues, data, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_uf_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_empresa(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_area(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_curso(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Genders", "Genero", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_genero(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Classes", "Classe", contextName)
        dictValues, newData = IdadeDadosComparativos.campo_classe(dictValues, newData, request, contextName)

        dictValues["Total"] = IdadeDadosComparativos.campo_total(request, contextName)

        dictValues = IdadeDadosComparativos.campo_entidade_comparacao(dictValues, request, contextName)

        if newData.items() == 0:
            noInfo = True

        if dictValues["Entity"] in newData:
            complementData = newData.groupby([dictValues["Entity"]], dropna=True).agg({dictValues["Entity"]: 'first', 'Idade': 'sum'})
            newData = newData.groupby([dictValues["Entity"], 'Idade'], dropna=True).sum()
            newData = newData.groupby([dictValues["Entity"]], dropna=True).sum()

            newData = newData['Count'].nlargest(dictValues["Total"])
        else:
            newData = []
            complementData = []
            noInfo = True

        return dictValues, complementData, newData, noInfo