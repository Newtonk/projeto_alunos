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
    def campo_total(request, context):
        total = get_value_int("Total", 'qtyAgeDataComparation', 10, request, "idadeXdadosCompare", context)
        return total

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, context):
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            selectedState = get_value_string("CompanyState", "statesAgeDataComparation", "Todos", request, "idadeXdadosCompare", context)
            if selectedState not in data.Estado_Empresa.values and selectedState != "Todos":
                selectedState = "Todos"
        if selectedState != "Todos":
            data = data[data.Estado_Empresa == selectedState]

        dictValues["CompanyState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_empresa(dictValues, data, request, context):
        selectedCompany = "Todos"
        if checa_valor("Empresa", data):
            selectedCompany = get_value_string("Company", "companyAgeDataComparation", "Todos", request, "idadeXdadosCompare", context)
            if selectedCompany not in data.Empresa.values and selectedCompany != "Todos":
                selectedCompany = "Todos"
        if selectedCompany != "Todos":
            data = data[data.Empresa == selectedCompany]

        dictValues["Company"] = selectedCompany
        return dictValues, data

    @staticmethod
    def campo_area(dictValues, data, request, context):
        selectedArea = "Todos"
        if checa_valor("Area", data):
            selectedArea = get_value_string("Area", "areaAgeDataComparation", "Todos", request, "idadeXdadosCompare", context)
            if selectedArea not in data.Area.values and selectedArea != "Todos":
                selectedArea = "Todos"
        if selectedArea != "Todos":
            data = data[data.Area == selectedArea]

        dictValues["Area"] = selectedArea
        return dictValues, data

    @staticmethod
    def campo_uf_universidade(dictValues, data, request, context):
        selectedState = "Todos"
        if checa_valor("Estado_Universidade", data):
            selectedState = get_value_string("UniversityState", "statesUniAgeDataComparation", "Todos", request,
                                             "idadeXdadosCompare", context)
            if selectedState not in data.Estado_Universidade.values and selectedState != "Todos":
                selectedState = "Todos"
        if selectedState != "Todos":
            data = data[data.Estado_Universidade == selectedState]

        dictValues["UniversityState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_universidade(dictValues, data, request, context):
        selectedUniversity = "Todos"
        if checa_valor("Instituicao", data):
            selectedUniversity = get_value_string("University", "universityAgeDataComparation", "Todos", request,
                                                  "idadeXdadosCompare", context)
            if selectedUniversity not in data.Instituicao.values and selectedUniversity != "Todos":
                selectedUniversity = "Todos"
        if selectedUniversity != "Todos":
            data = data[data.Instituicao == selectedUniversity]

        dictValues["University"] = selectedUniversity
        return dictValues, data

    @staticmethod
    def campo_curso(dictValues, data, request, context):
        selectedCurso = "Todos"
        if checa_valor("Curso", data):
            selectedCurso = get_value_string("Course", "courseAgeDataComparation", "Todos", request,
                                             "idadeXdadosCompare", context)
            if selectedCurso not in data.Curso.values and selectedCurso != "Todos":
                selectedCurso = "Todos"
        if selectedCurso != "Todos":
            data = data[data.Curso == selectedCurso]

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def campo_classe(dictValues, data, request, context):
        selectedClass = "Todos"
        if checa_valor("Classe", data):
            selectedClass = get_value_string("Class", "classAgeDataComparation", "Todos", request,
                                              "idadeXdadosCompare", context)
            if selectedClass not in data.Classe.values and selectedClass != "Todos":
                selectedClass = "Todos"
        if selectedClass != "Todos":
            data = data[data.Classe == selectedClass]

        dictValues["Class"] = selectedClass

        return dictValues, data

    @staticmethod
    def campo_genero(dictValues, data, request, context):
        selectedGender = "Todos"
        if checa_valor("Genero", data):
            selectedGender = get_value_string("Gender", "genderAgeDataComparation", "Todos", request,
                                             "idadeXdadosCompare", context)
            if selectedGender not in data.Genero.values and selectedGender != "Todos":
                selectedGender = "Todos"
        if selectedGender != "Todos":
            data = data[data.Genero == selectedGender]

        dictValues["Gender"] = selectedGender
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(dictValues, request, context):
        selectedEntity = get_value_string("Entity", "entityAgeDataComparation", "Empresa", request, "idadeXdadosCompare", context)
        dictValues["Entity"] = selectedEntity

        return dictValues

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        dictValues = {}
        noInfo = False

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa")
        dictValues, newData = IdadeDadosComparativos.campo_uf_empresa(dictValues, data, request, context)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade")
        dictValues, newData = IdadeDadosComparativos.campo_uf_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa")
        dictValues, newData = IdadeDadosComparativos.campo_empresa(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao")
        dictValues, newData = IdadeDadosComparativos.campo_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area")
        dictValues, newData = IdadeDadosComparativos.campo_area(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso")
        dictValues, newData = IdadeDadosComparativos.campo_curso(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Genders", "Genero")
        dictValues, newData = IdadeDadosComparativos.campo_genero(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Classes", "Classe")
        dictValues, newData = IdadeDadosComparativos.campo_classe(dictValues, newData, request, context)

        dictValues["Total"] = IdadeDadosComparativos.campo_total(request, context)

        dictValues = IdadeDadosComparativos.campo_entidade_comparacao(dictValues, request, context)

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