

def pegue_todas_colunas(columns, data):
    colunasExistentes = []
    for column in columns:
        if checa_valor(column, data):
            colunasExistentes.append(column)
    return colunasExistentes

def checa_valor(value, data):
    if value not in data or data[value].count() == 0:
        return False
    return True

def get_value_string(objName , key, defaultValue, request, contextName, context):
    finalValue = defaultValue
    if key in request.POST:
        finalValue = request.POST[key]
    elif context[contextName] is not None:
        finalValue = context[contextName][objName]
    return finalValue


def get_value_int(objName , key, defaultValue, request, contextName, context):
    finalValue = defaultValue
    if key in request.POST:
        finalValue = int(request.POST[key])
    elif context[contextName] is not None:
        finalValue = context[contextName][objName]
    return finalValue

def get_unique_values(dictValues, data, tag, labelFile):
    if checa_valor(labelFile, data):
        dictValues[tag] = data[labelFile].dropna().unique()
    else:
        dictValues[tag] = []
    return dictValues