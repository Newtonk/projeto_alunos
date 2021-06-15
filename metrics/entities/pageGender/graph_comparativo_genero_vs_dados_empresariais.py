from metrics.utils import *

class GeneroDadosComparativosEmpresariais():
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Area', 'Empresa', "Instituicao", "Curso", "Genero", "Estado_Empresa", "Estado_Universidade", "Classe"], data)
        if "Genero" in colunas and ("Area" in colunas or "Empresa" in colunas or "Curso" in colunas or "Instituicao" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Genero', 'Area', "Curso" , "Empresa", "Instituicao", "Estado_Empresa" , "Estado_Universidade", "Classe"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_genero(dictValues, data, request, context):
        genders = data.Genero.dropna().unique()
        gender = get_value_string("Gender", 'genderLaborMarketComparation', genders[0], request, "generoXmercadodetrabalhoCompare", context)
        dictValues["Gender"] = gender
        dictValues["Genders"] = genders
        return dictValues

    @staticmethod
    def campo_total(request, context):
        total = get_value_int("Total", 'qtygenderLaborMarketComparation', 10, request, "generoXmercadodetrabalhoCompare", context)
        return total

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, context):
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            selectedState = get_value_string("CompanyState", "statesCompanyLaborMarketComparation", "Todos", request, "generoXmercadodetrabalhoCompare", context)
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
            selectedCompany = get_value_string("Company", "companyGenderXLaborMarketComparation", "Todos", request, "generoXmercadodetrabalhoCompare", context)
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
            selectedArea = get_value_string("Area", "areaGenderXLaborMarketComparation", "Todos", request, "generoXmercadodetrabalhoCompare", context)
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
            selectedState = get_value_string("UniversityState", "statesUniLaborMarketComparation", "Todos", request,
                                             "generoXmercadodetrabalhoCompare", context)
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
            selectedUniversity = get_value_string("University", "universityGenderXLaborMarketComparation", "Todos", request,
                                                  "generoXmercadodetrabalhoCompare", context)
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
            selectedCurso = get_value_string("Course", "courseGenderXLaborMarketComparation", "Todos", request,
                                             "generoXmercadodetrabalhoCompare", context)
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
            selectedClass = get_value_string("Class", "classGenderXLaborMarketComparation", "Todos", request,
                                             "generoXmercadodetrabalhoCompare", context)
            if selectedClass not in data.Classe.values and selectedClass != "Todos":
                selectedClass = "Todos"
        if selectedClass != "Todos":
            data = data[data.Classe == selectedClass]

        dictValues["Class"] = selectedClass
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(dictValues, request, context):
        selectedEntity = get_value_string("Entity", "entitygenderLaborMarketComparation", "Empresa", request, "generoXmercadodetrabalhoCompare", context)
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
        elif selectedEntity == "Classe":
            dictValues["Class"] = "Todos"
            dictValues["Classes"] = []

        return dictValues

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        dictValues = {}
        noInfo = False

        dictValues = GeneroDadosComparativosEmpresariais.campo_genero(dictValues, data, request, context)

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_uf_empresa(dictValues, data, request, context)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_uf_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_empresa(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_area(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_curso(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Classes", "Classe")
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_classe(dictValues, newData, request, context)

        dictValues["Total"] = GeneroDadosComparativosEmpresariais.campo_total(request, context)

        dictValues = GeneroDadosComparativosEmpresariais.campo_entidade_comparacao(dictValues, request, context)

        if newData.items() == 0:
            noInfo = True

        if dictValues["Entity"] in newData:
            complementData = newData.groupby([dictValues["Entity"], 'Genero']).sum()
            newData = complementData.groupby([dictValues["Entity"]]).sum()

            newData = newData['Count'].nlargest(dictValues["Total"])
        else:
            newData = []
            complementData = []
            noInfo = True

        return dictValues, complementData, newData, noInfo

