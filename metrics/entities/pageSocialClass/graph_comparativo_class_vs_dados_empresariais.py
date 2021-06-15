from metrics.utils import *

class ClasseDadosComparativos():
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Area', 'Empresa', "Instituicao", "Curso", "Classe", "Estado_Empresa", "Estado_Universidade", "Genero"], data)
        if "Classe" in colunas and ("Area" in colunas or "Empresa" in colunas or "Curso" in colunas or "Instituicao" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Classe', 'Area', "Curso", "Empresa", "Instituicao", "Estado_Empresa" , "Estado_Universidade", "Genero"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_total(request, context):
        total = get_value_int("Total", 'qtyclassLaborMarketComparation', 10, request, "classeXmercadodetrabalhoCompare", context)
        return total

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, context):
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            selectedState = get_value_string("CompanyState", "statesCompanyLaborMarketComparation", "Todos", request, "classeXmercadodetrabalhoCompare", context)
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
            selectedCompany = get_value_string("Company", "companyClassXLaborMarketComparation", "Todos", request, "classeXmercadodetrabalhoCompare", context)
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
            selectedArea = get_value_string("Area", "areaClassXLaborMarketComparation", "Todos", request, "classeXmercadodetrabalhoCompare", context)
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
            selectedState = get_value_string("UniversityState", "statesUniClassLaborMarketComparation", "Todos", request,
                                             "classeXmercadodetrabalhoCompare", context)
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
            selectedUniversity = get_value_string("University", "universityClassXLaborMarketComparation", "Todos", request,
                                                  "classeXmercadodetrabalhoCompare", context)
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
            selectedCurso = get_value_string("Course", "courseClassXLaborMarketComparation", "Todos", request,
                                             "classeXmercadodetrabalhoCompare", context)
            if selectedCurso not in data.Curso.values and selectedCurso != "Todos":
                selectedCurso = "Todos"
        if selectedCurso != "Todos":
            data = data[data.Curso == selectedCurso]

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def campo_classe(dictValues, data, request, context):
        classes = data.Classe.dropna().unique()
        selectedClass = get_value_string("Class", 'classClassXLaborMarketComparation', classes[0], request,
                                  "classeXmercadodetrabalhoCompare", context)
        dictValues["Class"] = selectedClass
        dictValues["Classes"] = classes
        return dictValues


    @staticmethod
    def campo_genero(dictValues, data, request, context):
        selectedGender = "Todos"
        if checa_valor("Genero", data):
            selectedGender = get_value_string("Gender", "genderClassLaborMarketComparation", "Todos", request,
                                             "classeXmercadodetrabalhoCompare", context)
            if selectedGender not in data.Genero.values and selectedGender != "Todos":
                selectedGender = "Todos"
        if selectedGender != "Todos":
            data = data[data.Genero == selectedGender]

        dictValues["Gender"] = selectedGender
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(dictValues, request, context):
        selectedEntity = get_value_string("Entity", "entityclassLaborMarketComparation", "Empresa", request, "classeXmercadodetrabalhoCompare", context)
        dictValues["Entity"] = selectedEntity
        if selectedEntity == "Empresa":
            dictValues["Company"] = "Todos"
            dictValues["Companies"] = []
        elif selectedEntity == "Instituicao":
            dictValues["University"] = "Todos"
            dictValues["Universities"] = []
        elif selectedEntity == "Area":
            dictValues["Area"] = "Todos"
            dictValues["Areas"] = []
        elif selectedEntity == "Curso":
            dictValues["Course"] = "Todos"
            dictValues["Courses"] = []
        elif selectedEntity == "Genero":
            dictValues["Gender"] = "Todos"
            dictValues["Genders"] = []

        return dictValues

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        dictValues = {}
        noInfo = False

        dictValues = ClasseDadosComparativos.campo_classe(dictValues, data, request, context)

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa")
        dictValues, newData = ClasseDadosComparativos.campo_uf_empresa(dictValues, data, request, context)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade")
        dictValues, newData = ClasseDadosComparativos.campo_uf_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa")
        dictValues, newData = ClasseDadosComparativos.campo_empresa(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao")
        dictValues, newData = ClasseDadosComparativos.campo_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area")
        dictValues, newData = ClasseDadosComparativos.campo_area(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso")
        dictValues, newData = ClasseDadosComparativos.campo_curso(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Genders", "Genero")
        dictValues, newData = ClasseDadosComparativos.campo_genero(dictValues, newData, request, context)

        dictValues["Total"] = ClasseDadosComparativos.campo_total(request, context)

        dictValues = ClasseDadosComparativos.campo_entidade_comparacao(dictValues, request, context)

        if newData.items() == 0:
            noInfo = True

        if dictValues["Entity"] in newData:
            complementData = newData.groupby([dictValues["Entity"], 'Classe']).sum()
            newData = complementData.groupby([dictValues["Entity"]]).sum()

            newData = newData['Count'].nlargest(dictValues["Total"])
        else:
            newData = []
            complementData = []
            noInfo = True

        return dictValues, complementData, newData, noInfo

