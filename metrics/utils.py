import json


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

def get_value_string(objName , key, defaultValue, request, contextName):
    finalValue = defaultValue
    if key in request.POST:
        finalValue = request.POST[key]
    elif contextName is not None:
        finalValue = contextName[objName]
    return finalValue

def get_multiple_value_string(objName , key, defaultValue, request, contextName):
    finalValue = [defaultValue]
    if key in request.POST:
        finalValue = json.loads(request.POST[key])
    elif contextName is not None:
        finalValue = contextName[objName]
    return finalValue


def get_value_int(objName , key, defaultValue, request, contextName):
    finalValue = defaultValue
    if key in request.POST:
        finalValue = int(request.POST[key])
    elif contextName is not None:
        finalValue = contextName[objName]
    return finalValue

def check_minium_values(listValues, data):

    for value in listValues:
        if value not in data or data[value].count() == 0:
            return False
    return True

def get_unique_values(dictValues, data, tag, labelFile, contextName):
    dictValues[tag] = {}
    if checa_valor(labelFile, data):
        dictValues[tag]["Item"] = list(data[labelFile].dropna().unique())
    else:
        dictValues[tag]["Item"] = []
    if contextName is not None and dictValues[tag]["Item"] == contextName[tag]["Item"]:
        dictValues[tag]["SameState"] = "True"
    else:
        dictValues[tag]["SameState"] = "False"
    return dictValues

def separate_single_value_secondary(value, data, tag, entity):
    newData = data
    if "Todos" != value:
        all_entities = list(data[data[tag] == value][entity].dropna().unique())
        if len(all_entities) > 0:
            newData = data[data[entity].isin(all_entities)]
            if newData.size == 0:
                newData = data
    return newData, value

def separate_single_value(value, data, tag):
    newData = data
    if "Todos" != value:
        newData = data[data[tag] == value]
        if newData.size == 0:
            newData = data
    return newData, value

def separate_values_into_list(list_values, data, tag):
    newData = data
    if "Todos" not in list_values:
        newData = data[data[tag].isin(list_values)]
        if newData.size == 0:
            list_values = ["Todos"]
            newData = data
        else:
            actual_values = list(newData[tag].dropna().unique())
            list_values = list(set(list_values) & set(actual_values))
    return newData, list_values