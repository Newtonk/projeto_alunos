from metrics.utils import *

class GeneroDadosComparativosEmpresariais():
    @staticmethod
    def validacao_colunas(entity, data, isInitial):
        colunas = pegue_todas_colunas(['Area', "Curso", "Empresa", "Universidade", "Estado_Empresa", "Estado_Universidade", "Classe"], data)
        if len(colunas) > 0 and checa_valor("Genero", data):
            if entity not in colunas and isInitial:
                entity = colunas[0]
            return True, entity
        return False, entity

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Genero', 'Area', "Curso", "Empresa", "Universidade", "Estado_Empresa", "Estado_Universidade", "Classe"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_genero(dictValues, data, request, contextName, entity):
        gender = get_value_string("Gender", 'genderLaborMarketComparation', dictValues["Genders"]["Item"][0], request, contextName)
        data, gender = separate_single_value_secondary(gender, data, "Genero", entity)
        dictValues["Gender"] = gender
        return dictValues, data

    @staticmethod
    def campo_total(request, contextName):
        total = get_value_int("Total", 'qtygenderLaborMarketComparation', 10, request, contextName)
        return total

    @staticmethod
    def campo_ordenacao(request, contextName):
        order = get_value_string("Order", 'maxMingenderLaborMarketComparation', "Max", request, contextName)
        return order

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
            selectedCompany = get_multiple_value_string("Company", "companyGenderXLaborMarketComparation", "Todos", request, contextName)
            data, selectedCompany = separate_values_into_list(selectedCompany, data, "Empresa")

        dictValues["Company"] = selectedCompany
        return dictValues, data

    @staticmethod
    def campo_area(dictValues, data, request, contextName):
        selectedArea = ["Todos"]
        if checa_valor("Area", data):
            selectedArea = get_multiple_value_string("Area", "areaGenderXLaborMarketComparation", "Todos", request, contextName)
            data, selectedArea = separate_values_into_list(selectedArea, data, "Area")

        dictValues["Area"] = selectedArea
        return dictValues, data

    @staticmethod
    def campo_uf_universidade(dictValues, data, request, contextName):
        selectedState = ["Todos"]
        if checa_valor("Estado_Universidade", data):
            selectedState = get_multiple_value_string("UniversityState", "statesUniLaborMarketComparation", "Todos", request,
                                             contextName)
            data, selectedState = separate_values_into_list(selectedState, data, "Estado_Universidade")

        dictValues["UniversityState"] = selectedState
        return dictValues, data

    @staticmethod
    def campo_universidade(dictValues, data, request, contextName):
        selectedUniversity = ["Todos"]
        if checa_valor("Universidade", data):
            selectedUniversity = get_multiple_value_string("University", "universityGenderXLaborMarketComparation", "Todos", request,
                                                  contextName)
            data, selectedUniversity = separate_values_into_list(selectedUniversity, data, "Universidade")

        dictValues["University"] = selectedUniversity
        return dictValues, data

    @staticmethod
    def campo_curso(dictValues, data, request, contextName):
        selectedCurso = ["Todos"]
        if checa_valor("Curso", data):
            selectedCurso = get_multiple_value_string("Course", "courseGenderXLaborMarketComparation", "Todos", request,
                                             contextName)
            data, selectedCurso = separate_values_into_list(selectedCurso, data, "Curso")

        dictValues["Course"] = selectedCurso
        return dictValues, data

    @staticmethod
    def campo_classe(dictValues, data, request, contextName):
        selectedClass = ["Todos"]
        if checa_valor("Classe", data):
            selectedClass = get_multiple_value_string("Class", "classGenderXLaborMarketComparation", "Todos", request,
                                             contextName)
            data, selectedClass = separate_values_into_list(selectedClass, data, "Classe")

        dictValues["Class"] = selectedClass
        return dictValues, data

    @staticmethod
    def campo_entidade_comparacao(request, contextName):
        selectedEntity = get_value_string("Entity", "entitygenderLaborMarketComparation", "Empresa", request, contextName)
        return selectedEntity

    @staticmethod
    def valida_dados_enviados(data, request, contextName, entityValue):
        newData = data
        dictValues = {}
        noInfo = False

        dictValues = get_unique_values(dictValues, data, "Genders", "Genero", contextName)

        dictValues = get_unique_values(dictValues, data, "CompanyStates", "Estado_Empresa", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_uf_empresa(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "UniversityStates", "Estado_Universidade", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_uf_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Companies", "Empresa", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_empresa(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Universities", "Universidade", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_universidade(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Areas", "Area", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_area(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Courses", "Curso", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_curso(dictValues, newData, request, contextName)

        dictValues = get_unique_values(dictValues, newData, "Classes", "Classe", contextName)
        dictValues, newData = GeneroDadosComparativosEmpresariais.campo_classe(dictValues, newData, request, contextName)

        dictValues["Total"] = GeneroDadosComparativosEmpresariais.campo_total(request, contextName)

        dictValues["Order"] = GeneroDadosComparativosEmpresariais.campo_ordenacao(request, contextName)

        if newData.items() == 0:
            noInfo = True

        if entityValue in newData:
            complementData = newData.groupby([entityValue, 'Genero']).sum()
            dictValues, newData = GeneroDadosComparativosEmpresariais.campo_genero(dictValues, newData, request, contextName, entityValue)
            newData = newData.groupby([entityValue, 'Genero']).sum()
            newData = newData.groupby([entityValue]).sum()

            newData = newData['Count'].nlargest(dictValues["Total"])
        else:
            newData = []
            complementData = []
            noInfo = True

        return dictValues, complementData, newData, noInfo

