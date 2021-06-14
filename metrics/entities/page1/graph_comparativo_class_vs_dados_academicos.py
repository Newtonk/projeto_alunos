from metrics.utils import *

class ClasseDadosComparativos():
    @staticmethod
    def validacao_colunas(data):
        colunas = pegue_todas_colunas(['Curso', 'Instituicao', "Classe", "Estado_Universidade"], data)
        if "Classe" in colunas and ("Curso" in colunas or "Instituicao" in colunas):
            return True
        return False

    @staticmethod
    def unifica_colunas(data):
        colunas = pegue_todas_colunas(['Classe', 'Curso', "Instituicao", "Estado_Universidade"], data)
        dados_unificados = data.groupby(colunas, dropna=False).size().reset_index(name='Count')
        return dados_unificados

    @staticmethod
    def campo_uf_universidade(data, request, context):
        states = []
        selectedState = "Todos"
        if checa_valor("Estado_Universidade", data):
            states = data.Estado_Universidade.dropna().unique()
            selectedState = get_value_string("State", "statesComparationInClass", "Todos", request, "classeXcursoCompare", context)
        if selectedState != "Todos":
            data = data[data.Estado_Universidade == selectedState]
        return states, selectedState, data

    @staticmethod
    def campo_classe(data, request, context):
        classes = data.Classe.dropna().unique()
        selectedClass = get_value_string("Class", 'classComparationInClass', classes[0], request, "classeXcursoCompare", context)
        return classes, selectedClass

    @staticmethod
    def campo_total(request, context):
        total = get_value_int("Total", 'qtyclasscoursecompare', 10, request, "classeXcursoCompare", context)
        return total

    @staticmethod
    def campo_curso(data, request, context):
        cursos = []
        selectedCurso = "Todos"
        if checa_valor("Curso", data):
            cursos = data.Curso.dropna().unique()
            selectedCurso = get_value_string("Course", "courseComparationInClass", "Todos", request, "classeXcursoCompare", context)
            if selectedCurso not in data.Curso.values and selectedCurso != "Todos":
                selectedCurso = cursos[0]
        if selectedCurso != "Todos":
            data = data[data.Curso == selectedCurso]

        return cursos, selectedCurso, data

    @staticmethod
    def campo_entidade_comparacao(request, context):
        selectedCurso = get_value_string("Entity", "entityComparationInClass", "Instituicao", request, "classeXcursoCompare", context)

        return selectedCurso

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = data
        selectedEntity = ClasseDadosComparativos.campo_entidade_comparacao(request, context)
        ufs = []
        cursos = []
        noInfo = False
        if selectedEntity == "Instituicao":
            classes, selectedClass = ClasseDadosComparativos.campo_classe(data, request, context)
            ufs, uf , newData = ClasseDadosComparativos.campo_uf_universidade(data, request, context)
            cursos, curso, newData = ClasseDadosComparativos.campo_curso(newData, request, context)
            total = ClasseDadosComparativos.campo_total(request, context)
        else:
            classes, selectedClass = ClasseDadosComparativos.campo_classe(data, request, context)
            uf = "Todos"
            curso = "Todos"
            total = ClasseDadosComparativos.campo_total(request,context)

        if selectedEntity in newData:
            complementData = newData.groupby([selectedEntity, 'Classe']).sum()
            newData = complementData.groupby([selectedEntity]).sum()

            newData = newData['Count'].nlargest(total)
        else:
            newData = []
            complementData = []
            noInfo = True

        return ufs, uf, cursos, curso, classes, selectedClass, total, selectedEntity, complementData, newData , noInfo

