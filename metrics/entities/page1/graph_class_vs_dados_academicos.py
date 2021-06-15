from metrics.utils import *

class ClasseDadosAcademicos:
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
            selectedState = get_value_string("State", "statesClassXCourse", "Todos", request, "classeXcurso", context)
        if selectedState != "Todos":
            data = data[data.Estado_Universidade == selectedState]
        return states, selectedState, data

    @staticmethod
    def campo_universidade(data, request, context):
        universities = []
        selectedUniversity = "Todos"
        if checa_valor("Instituicao", data):
            universities = data.Instituicao.dropna().unique()
            selectedUniversity = get_value_string("Instituicao", "universityClassXCourse", "Todos", request, "classeXcurso", context)
            if "statesClassXCourse" in request.POST and request.POST["statesClassXCourse"] != context["classeXcurso"]["State"]:
                selectedUniversity = "Todos"
        if selectedUniversity != "Todos":
            data = data[data.Instituicao == selectedUniversity]
        return universities, selectedUniversity, data

    @staticmethod
    def campo_curso(data, request, context):
        cursos = []
        selectedCurso = "Todos"
        if checa_valor("Curso", data):
            cursos = data.Curso.dropna().unique()
            selectedCurso = get_value_string("Course", "courseClassXCourse", "Todos", request, "classeXcurso", context)
            if selectedCurso not in data.Curso.values and selectedCurso != "Todos":
                selectedCurso = cursos[0]
        if selectedCurso != "Todos":
            data = data[data.Curso == selectedCurso]

        return cursos, selectedCurso, data

    @staticmethod
    def valida_dados_enviados(data, request, context):
        newData = None
        noInfo = False
        ufs, uf , newData = ClasseDadosAcademicos.campo_uf_universidade(data, request, context)
        universidades, universidade, newData = ClasseDadosAcademicos.campo_universidade(newData, request, context)
        cursos, curso, newData = ClasseDadosAcademicos.campo_curso(newData, request, context)

        if newData.items() == 0:
            noInfo = True

        colunas = pegue_todas_colunas(['Curso', 'Classe', "Instituicao", "Estado_Universidade"], data)
        if checa_valor("Curso", data):
            if curso == "Todos":
                colunas.remove("Curso")
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count']
            else:
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count'][curso]
        elif checa_valor("Instituicao", data):
            if universidade == "Todos":
                colunas.remove("Instituicao")
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count']
            else:
                colunas.remove("Instituicao")
                colunas.insert(0, "Instituicao")
                newData = newData.groupby(colunas, dropna=False).sum()
                newData = newData['Count'][universidade]
        return ufs, uf, universidades, universidade, cursos, curso, newData, noInfo

