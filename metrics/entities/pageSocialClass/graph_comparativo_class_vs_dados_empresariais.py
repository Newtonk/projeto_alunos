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
    def campo_total(request, contextName):
        total = get_value_int("Total", 'qtyclassLaborMarketComparation', 10, request, contextName)
        return total

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Empresa", data):
            selectedState = get_multiple_value_string("CompanyState", "statesCompanyLaborMarketComparation", "Todos", request, contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Empresa")

        dictValues["CompanyState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_empresa(dictValues, data, request, contextName):
        selectedCompany = ["Todos"]
        if checa_valor("Empresa", data):
            selectedCompany = get_multiple_value_string("Company", "companyClassXLaborMarketComparation", "Todos", request, contextName)
            data, selectedCompany = separate_values_into_list(selectedCompany, data, "Empresa")

        dictValues["Company"] = selectedCompany
        return dictValues, data

    @staticmethod
    def campo_area(dictValues, data, request, contextName):
        selectedArea = "Todos"
        if checa_valor("Area", data):
            selectedArea = get_multiple_value_string("Area", "areaClassXLaborMarketComparation", "Todos", request, contextName)
            data, selectedArea = separate_values_into_list(selectedArea, data, "Area")

        dictValues["Area"] = selectedArea
        return dictValues, data

    @staticmethod
    def campo_uf_universidade(dictValues, data, request, contextName):
        selectedState = "Todos"
        if checa_valor("Estado_Universidade", data):
            selectedState = get_multiple_value_string("UniversityState", "statesUniClassLaborMarketComparation", "Todos", request, contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Universidade")

        dictValues["UniversityState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_universidade(dictValues, data, request, contextName):
        selectedUniversity = "Todos"
        if checa_valor("Instituicao", data):
            selectedUniversity = get_multiple_value_string("University", "universityClassXLaborMarketComparation", "Todos", request, contextName)
            data, selectedUniversity = separate_values_into_list(selectedUniversity, data, "Instituicao")

        dictValues["University"] = selectedUniversity
        return dictValues, data

    @staticmethod
    def campo_curso(dictValues, data, request, contextName):
        selectedCurso = "Todos"
        if checa_valor("Curso", data):
            selectedCurso = get_multiple_value_string("Course", "courseClassXLaborMarketComparation", "Todos", request, contextName)
            data, selectedCurso = separate_values_into_list(selectedCurso, data, "Curso")

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def campo_classe(dictValues, data, request, contextName):
        dictValues = get_unique_values(dictValues, data, "Classes", "Classe", contextName)
        selectedClass = get_value_string("Class", 'classClassXLaborMarketComparation', dictValues["Classes"]["Item"][0], request, contextName)
        data, selectedClass = separate_single_value(selectedClass, data, "Classe")
        dictValues["Class"] = selectedClass
        return dictValues


    @staticmethod
    def campo_genero(dictValues, data, request, contextName):
        selectedGender = "Todos"
        if checa_valor("Genero", data):
            selectedGender = get_multiple_value_string("Gender", "genderClassLaborMarketComparation", "Todos", request, contextName)
            data, selectedGender = separate_values_into_list(selectedGender, data, "Genero")

        dictValues["Gender"] = selectedGender
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(dictValues, request, contextName):
        selectedEntity = get_value_string("Entity", "entityclassLaborMarketComparation", "Empresa", request, contextName)
        dictValues["Entity"] = selectedEntity

        return dictValues

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        dictValues = {}
        noInfo = False
        contextName = context["classeXmercadodetrabalhoCompare"]

        dictValues = ClasseDadosComparativos.campo_classe(dictValues, data, request, contextName)

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_uf_empresa(dictValues, data, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_uf_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_empresa(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_area(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_curso(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Genders", "Genero", contextName)
        dictValues, newData = ClasseDadosComparativos.campo_genero(dictValues, newData, request, contextName)

        dictValues["Total"] = ClasseDadosComparativos.campo_total(request, contextName)

        dictValues = ClasseDadosComparativos.campo_entidade_comparacao(dictValues, request, contextName)

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

