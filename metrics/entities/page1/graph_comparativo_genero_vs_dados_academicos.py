from metrics.utils import *

class GeneroDadosComparativos():
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Curso', 'Instituicao', "Genero", "Estado_Universidade"], data)
        if "Genero" in colunas and ("Curso" in colunas or "Instituicao" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Genero', 'Curso', "Instituicao", "Estado_Universidade"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_uf_universidade(data, request, context):
        states = []
        selectedState = "Todos"
        if checa_valor("Estado_Universidade", data):
            states = data.Estado_Universidade.dropna().unique()
            selectedState = get_value_string("State", "statesComparation", "Todos", request, "generoXcursoCompare", context)
        if selectedState != "Todos":
            data = data[data.Estado_Universidade == selectedState]
        return states, selectedState, data

    @staticmethod
    def campo_genero(data, request, context):
        genders = data.Genero.dropna().unique()
        gender = get_value_string("Gender", 'genderComparation', genders[0], request, "generoXcursoCompare", context)
        return genders, gender

    @staticmethod
    def campo_total(request, context):
        total = get_value_int("Total", 'qtygenderCourseComparation', 10, request, "generoXcursoCompare", context)
        return total

    @staticmethod
    def campo_curso(data, request, context):
        cursos = []
        selectedCurso = "Todos"
        if checa_valor("Curso", data):
            cursos = data.Curso.dropna().unique()
            selectedCurso = get_value_string("Course", "courseComparation", "Todos", request, "generoXcursoCompare", context)
            if selectedCurso not in data.Curso.values and selectedCurso != "Todos":
                selectedCurso = cursos[0]
        if selectedCurso != "Todos":
            data = data[data.Curso == selectedCurso]

        return cursos, selectedCurso, data

    @staticmethod
    def campo_entidade_comparacao(request, context):
        selectedCurso = get_value_string("Entity", "entitygenderComparation", "Instituicao", request, "generoXcursoCompare", context)

        return selectedCurso

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        selectedEntity = GeneroDadosComparativos.campo_entidade_comparacao(request, context)
        ufs = []
        cursos = []
        noInfo = False
        if selectedEntity == "Instituicao":
            generos, genero = GeneroDadosComparativos.campo_genero(data, request, context)
            ufs, uf , newData = GeneroDadosComparativos.campo_uf_universidade(data, request, context)
            cursos, curso, newData = GeneroDadosComparativos.campo_curso(newData, request, context)
            total = GeneroDadosComparativos.campo_total(request, context)
        else:
            generos, genero = GeneroDadosComparativos.campo_genero(data, request, context)
            uf = "Todos"
            curso = "Todos"
            total = GeneroDadosComparativos.campo_total(request,context)

        if selectedEntity in newData:
            complementData = newData.groupby([selectedEntity, 'Genero']).sum()
            newData = complementData.groupby([selectedEntity]).sum()

            newData = newData['Count'].nlargest(total)
        else:
            newData = []
            complementData = []
            noInfo = True

        return ufs, uf, cursos, curso, generos, genero, total, selectedEntity, complementData, newData, noInfo

