import json
import yaml

f = open('myparamfile.json')
dataParam = json.load(f)
f.close()

with open('mytemplatefile.yaml', 'r') as y:
    dataTemplate = yaml.load(y, Loader=yaml.BaseLoader)

paramListInParamFile = []
for k in dataParam:
    paramListInParamFile.append(k['ParameterKey'])

paramListInTemplateFile = []
for kk in dataTemplate['Parameters']:
    paramListInTemplateFile.append(kk)

paramListInParamFile.sort()
paramListInTemplateFile.sort()

if paramListInParamFile == paramListInTemplateFile:
    print ("Same parameters on both files")
else:
    print ("Differences in parameters between both files !")

    resultNotInParamFile = [x for x in paramListInTemplateFile if x not in paramListInParamFile]
    if len(resultNotInParamFile) != 0:
        resultNotInParamFileStr = ' '.join(map(str, resultNotInParamFile))
        print("List of keys that are not present in the param file but are in the template : " + resultNotInParamFileStr)

    resultNotInTemplateFile = [x for x in paramListInParamFile if x not in paramListInTemplateFile]
    if len(resultNotInTemplateFile) != 0:
        resultNotInTemplateFileStr = ' '.join(map(str, resultNotInTemplateFile))
        print("List of keys that are not present in the template but present in param file : " + resultNotInTemplateFileStr)