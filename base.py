from flask import Flask, render_template, url_for, redirect, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re

app=Flask(__name__)


def showing(sur="", all=0):
    r = requests.get(url = "http://localhost:8090/baseDstu3/Patient?_count=1000000", params = "")

    PatientData=[]
    for x in r.json()['entry']:
        if (all==1 or re.search(sur, str(x['resource']['name'][0]['family'])) or re.search(sur, str(x['resource']['name'][0]['given']))):
            temp={}
            PatientData.append(temp)
            temp['Name']=str(x['resource']['name'][0]['given'][0])
            temp['Surname']=str(x['resource']['name'][0]['family'])
            temp['Id']=str(x['resource']['identifier'][0]['value'])
    return PatientData

def showingObservation(s, sur="", all=0):
    r = requests.get(url = f"http://localhost:8090/baseDstu3/Observation?patient.identifier={s}", params = "")

    PatientData=[]
    for x in r.json()['entry']:
        if (True or all==1 or re.search(sur, str(x['resource']['name'][0]['family'])) or re.search(sur, str(x['resource']['name'][0]['given']))):
            temp={}
            PatientData.append(temp)
            temp['Display']=str(x['resource']['code']['text'])
            temp['Date']=str(x['resource']['effectiveDateTime'])
            try:
                temp['Value']=f"{x['resource']['valueQuantity']['value']} [{x['resource']['valueQuantity']['code']}]" 
            except:
                if temp['Display'] == "Blood Pressure":
                    zisDict=x['resource']['component']
                    temp['Display']=zisDict[0]['code']['text']
                    temp['Value']=f"{zisDict[0]['valueQuantity']['value']} [{zisDict[0]['valueQuantity']['code']}]"

                    temp2=temp.copy()
                    temp2['Display']=zisDict[1]['code']['text']
                    temp2['Value']=f"{zisDict[1]['valueQuantity']['value']} [{zisDict[1]['valueQuantity']['code']}]"
                    PatientData.append(temp2)
                else:    
                    temp['Value']=""
    return PatientData


def showingMedicationR(s, sur="", all=0):
    r = requests.get(url = f"http://localhost:8090/baseDstu3/MedicationRequest?patient.identifier={s}", params = "")

    PatientData=[]
    for x in r.json()['entry']:
        if (True or all==1 or re.search(sur, str(x['resource']['name'][0]['family'])) or re.search(sur, str(x['resource']['name'][0]['given']))):
            temp={}
            PatientData.append(temp)
            temp['Date']=str(x['resource']['authoredOn'])
            temp['Status']=str(x['resource']['status'])
            temp['Medication']=f"{x['resource']['medicationCodeableConcept']['coding'][0]['text']}"
            try:
                temp['dosageInstruction']=f"{x['resource']['dosageInstruction']['additionalInstruction']['text']}" 
            except:
                temp['dosageInstruction']=""

    return PatientData


#href=f"http://localhost:8090/baseDstu3/Observation?patient.identifier={y[x]}"
def createElem(doc, tab, elemList, namez=['Name', 'Surname', 'Id']):
    print(tab)
    for y in elemList:
        trow = doc.new_tag("tr")
        tab.append(trow)
        for x in namez:
            info=doc.new_tag("td")
            if (x=='Id'):
                #link=doc.new_tag("button", form="page", formmethod="post", type="submit", name="next", value=y[x])
                link=doc.new_tag("button", attrs={"form":"page", "formmethod":"post", "type":"submit", "name":"next", "value":y[x]})
                link.string=y[x]
                info.append(link)
            else:
                info.string=y[x]
            trow.append(info)

@app.route('/', methods=['GET', 'POST'])
def Wisdom():
    req=request
    html_doc=open('./templates/index.html')
    souper=BeautifulSoup(html_doc, 'html.parser')

    data=souper.find("tbody", id="Patients")
    if (req.method=='POST'):
        s=req.form['next']
        if (s=='search'):
            jsonInfo=showing(sur=req.form['Surname'])
            createElem(souper, data, jsonInfo)
        else:
            jsonInfo=showingObservation(s)
            data=souper.find("tbody", id="Observation")
            createElem(souper, data, jsonInfo, ['Display', 'Date', 'Value'])
            #data.string=f"http://localhost:8090/baseDstu3/Observation?patient.identifier={s}"
    
        return render_template_string(souper.prettify())

    else:
        jsonInfo=showing(all=1)
        createElem(souper, data, jsonInfo)

        return render_template_string(souper.prettify())


if __name__=='__main__':
    app.run()
