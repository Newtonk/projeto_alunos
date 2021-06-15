from metrics.utils import *

class GeneroDadosEmpresariais:
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Area', 'Empresa', "Instituicao" , "Curso", "Genero", "Estado_Empresa" , "Estado_Universidade"], data)
        if "Genero" in colunas and ("Area" in colunas or "Empresa" in colunas or "Curso" in colunas or "Instituicao" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Genero', 'Area', "Curso" , "Empresa", "Instituicao", "Estado_Empresa" , "Estado_Universidade"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_uf_empresa(dictValues, data, request, context):
        selectedState = "Todos"
        if checa_valor("Estado_Empresa", data):
            selectedState = get_value_string("CompanyState", "statesGenderXLaborMarket", "Todos", request,
                                             "generoXmercadodetrabalho", context)
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
            selectedCompany = get_value_string("Company", "companyGenderXLaborMarket", "Todos", request,
                                               "generoXmercadodetrabalho", context)
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
            selectedArea = get_value_string("Area", "areaGenderXLaborMarket", "Todos", request,
                                            "generoXmercadodetrabalho", context)
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
            selectedState = get_value_string("UniversityState", "statesUniGenderXLaborMarket", "Todos", request,
                                             "generoXmercadodetrabalho", context)
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
            selectedUniversity = get_value_string("University", "universityGenderXLaborMarket", "Todos",
                                                  request,
                                                  "generoXmercadodetrabalho", context)
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
            selectedCurso = get_value_string("Course", "courseGenderXLaborMarket", "Todos", request,
                                             "generoXmercadodetrabalho", context)
            if selectedCurso not in data.Curso.values and selectedCurso != "Todos":
                selectedCurso = "Todos"
        if selectedCurso != "Todos":
            data = data[data.Curso == selectedCurso]

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = None
        noInfo = False
        dictValues = {}

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa")
        dictValues, newData = GeneroDadosEmpresariais.campo_uf_empresa(dictValues, data, request, context)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade")
        dictValues, newData = GeneroDadosEmpresariais.campo_uf_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa")
        dictValues, newData = GeneroDadosEmpresariais.campo_empresa(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Instituicao")
        dictValues, newData = GeneroDadosEmpresariais.campo_universidade(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area")
        dictValues, newData = GeneroDadosEmpresariais.campo_area(dictValues, newData, request, context)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso")
        dictValues, newData = GeneroDadosEmpresariais.campo_curso(dictValues, newData, request, context)


        if newData.items() == 0:
            noInfo = True

        colunas = pegue_todas_colunas(['Genero'], data)
        newData = newData.groupby(colunas, dropna=True).sum()
        newData = newData['Count']
        return dictValues, newData, noInfo

