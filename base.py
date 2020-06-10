from flask import Flask, render_template, url_for, redirect, request, render_template_string
import requests
from bs4 import BeautifulSoup
import re
import time
import os

app=Flask(__name__)

patientId="whatever"

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

def showingObservation(s, sur="", all=0, minDate="1928-04-28", maxDate="2112-04-28", minDateHeight="1928-04-28", maxDateHeight="2112-04-28", minDateWeight="1928-04-28", maxDateWeight="2112-04-28"):
    r = requests.get(url = f"http://localhost:8090/baseDstu3/Observation?patient.identifier={s}&_count=1000000", params = "")
    minDateTime=time.strptime(minDate, "%Y-%m-%d")
    maxDateTime=time.strptime(maxDate, "%Y-%m-%d")
    minDateTimeHeight=time.strptime(minDateHeight, "%Y-%m-%d")
    maxDateTimeHeight=time.strptime(maxDateHeight, "%Y-%m-%d")
    minDateTimeWeight=time.strptime(minDateWeight, "%Y-%m-%d")
    maxDateTimeWeight=time.strptime(maxDateWeight, "%Y-%m-%d")

    # body height creator
    plotData_height = [["date","close"]]
    for x in r.json()['entry']:
        Observ_date_string = str(x['resource']['effectiveDateTime'])
        Observ_date=time.strptime(Observ_date_string[:10], "%Y-%m-%d")
        display = str(x['resource']['code']['text'])
        if (maxDateTimeHeight < Observ_date or Observ_date < minDateTimeHeight):
            continue
        if(display == "Body Height"):
            plotData_height.append([ Observ_date_string[:10], str(x['resource']['valueQuantity']['value']) ])
    with open('data_height.csv','w') as f:
        f.write('\n'.join([','.join(x) for x in plotData_height]))

    # body weight creator
    plotData_weight = [["date","close"]]
    for x in r.json()['entry']:
        Observ_date_string = str(x['resource']['effectiveDateTime'])
        Observ_date=time.strptime(Observ_date_string[:10], "%Y-%m-%d")
        display = str(x['resource']['code']['text'])
        if (maxDateTimeWeight < Observ_date or Observ_date < minDateTimeWeight):
            continue
        if(display == "Body Weight"):
            plotData_weight.append([ Observ_date_string[:10], str(x['resource']['valueQuantity']['value']) ])
    with open('data_weight.csv','w') as f:
        f.write('\n'.join([','.join(x) for x in plotData_weight]))

    PatientData=[]
    for x in r.json()['entry']:
        #if ()
        if (True or all==1 or re.search(sur, str(x['resource']['code']['text']))):
            Observ_date=time.strptime(str(x['resource']['effectiveDateTime'])[:10], "%Y-%m-%d")
            if (maxDateTime < Observ_date or Observ_date < minDateTime):
                continue

            temp={}
            PatientData.append(temp)
            temp['Display']=str(x['resource']['code']['text'])
            temp['Date']=str(x['resource']['effectiveDateTime'])
            # if(len(x['resource']['component']) != 0):
            #     temp['Component']['Text'] = list()
            #     temp['Component']['Value'] = list()
            #     for comp in x['resource']['component']:
            #         temp['Component']['Text'].append(comp['code']['text'])
            #         temp['Component']['Value'].append(f"{comp['valueQuantity']['value']} [{comp['valueQuantity']['code']}]")
            
            
            
            
            

            try:
                temp['Value']=f"{x['resource']['valueQuantity']['value']} [{x['resource']['valueQuantity']['code']}]" 
            except:
                if temp['Display'] in ["Tobacco smoking status NHIS",
                                         "Appearance of Urine", 
                                         "Odor of Urine", 
                                         "Clarity of Urine", 
                                         "Color of Urine",
                                          "Glucose [Presence] in Urine by Test strip",
                                          "Bilirubin.total [Presence] in Urine by Test strip",
                                          "Ketones [Presence] in Urine by Test strip",
                                          "Protein [Presence] in Urine by Test strip",
                                          "Nitrite [Presence] in Urine by Test strip",
                                          "Hemoglobin [Presence] in Urine by Test strip",
                                          "Leukocyte esterase [Presence] in Urine by Test strip"
                                          ]:
                    # zisDict=x['resource']['component']
                    # temp['Display']=zisDict[0]['code']['text']
                    # temp['Value']=f"{zisDict[0]['valueQuantity']['value']} [{zisDict[0]['valueQuantity']['code']}]"

                    # temp2=temp.copy()
                    # temp2['Display']=zisDict[1]['code']['text']
                    # temp2['Value']=f"{zisDict[1]['valueQuantity']['value']} [{zisDict[1]['valueQuantity']['code']}]"
                    # PatientData.append(temp2)
                    temp['Value']=""
                else:
                    print(temp['Display'])
                    temp['Value']=""
                    temp['Component'] = {}   
                    temp['Component']['Text'] = list()
                    temp['Component']['Value'] = list()
                    for comp in x['resource']['component']:
                        temp['Component']['Text'].append(comp['code']['text'])
                        temp['Component']['Value'].append(f"{comp['valueQuantity']['value']} [{comp['valueQuantity']['code']}]") 
    
    return PatientData


def showingMedicationR(s, sur="", all=0, minDate="1928-04-28", maxDate="2112-04-28"):
    r = requests.get(url = f"http://localhost:8090/baseDstu3/MedicationRequest?patient.identifier={s}&_count=1000000", params = "")
    minDateTime=time.strptime(minDate, "%Y-%m-%d")
    maxDateTime=time.strptime(maxDate, "%Y-%m-%d")

    PatientData=[]
    if not 'entry' in r.json():
        return
    for x in r.json()['entry']:
        if (True or all==1 or re.search(sur, str(x['resource']['name'][0]['family'])) or re.search(sur, str(x['resource']['name'][0]['given']))):
            Observ_date=time.strptime(str(x['resource']['authoredOn'])[:10], "%Y-%m-%d")
            if (maxDateTime < Observ_date or Observ_date < minDateTime):
                continue

            temp={}
            PatientData.append(temp)
            temp['Date']=str(x['resource']['authoredOn'])
            temp['Status']=str(x['resource']['status'])
            temp['Medication']=f"{x['resource']['medicationCodeableConcept']['text']}"
            try:
                dct = x['resource']['dosageInstruction'][0]['timing']['repeat']
                temp['Timing']=f"frequency: {dct['frequency']}  period: {dct['period']}  periodUnit: {dct['periodUnit']}" 
            except:
                temp['Timing']=""
            try:
                temp['dosageInstruction']=f"{x['resource']['dosageInstruction'][0]['additionalInstruction'][0]['text']}" 
            except:
                temp['dosageInstruction']=""

    return PatientData


#href=f"http://localhost:8090/baseDstu3/Observation?patient.identifier={y[x]}"
def createElem(doc, tab, elemList, namez=['Name', 'Surname', 'Id']):
    currentClass="0"
    if not elemList:
        return
    for y in elemList:
        trow = doc.new_tag("tr")
        trow['class']=currentClass
        tab.append(trow)
        for x in namez:
            if ('Component' in y and x=='Component'):
                for t, v in zip(y[x]['Text'], y[x]['Value']):
                    trow_inner = doc.new_tag("tr")
                    info1=doc.new_tag("td")
                    info_text=doc.new_tag("td")
                    info_text.string=t

                    info_value=doc.new_tag("td")
                    info_value.string=v
                    _=[trow_inner.append(x) for x in [info1, info_text, info_value]]

                    trow_inner['class']=currentClass
                    tab.append(trow_inner)

            elif (x!='Component'):
                info=doc.new_tag("td")
                if (x=='Id'):
                    #link=doc.new_tag("button", form="page", formmethod="post", type="submit", name="next", value=y[x])
                    link=doc.new_tag("button", attrs={"form":"page", "formmethod":"post", "type":"submit", "name":"next", "value":y[x]})
                    link.string=y[x]
                    info.append(link)
                else:
                    info.string=y[x]
                trow.append(info)
        currentClass=str(int(currentClass)+1)

@app.route('/', methods=['GET', 'POST'])
def Wisdom():
    req=request
    html_doc=open('./templates/index.html')
    souper=BeautifulSoup(html_doc, 'html.parser')
    global patientId

    data=souper.find("tbody", id="Patients")
    med_data=souper.find("tbody", id="Medication")
    if (req.method=='POST'):
        s=req.form['next']
        if (s=='search'):
            jsonInfo=showing(sur=req.form['Surname'])
            createElem(souper, data, jsonInfo)


        elif (s=='searchTime'):
            jsonInfo=showingObservation(patientId, minDate=req.form['MinDate'], 
                                                   maxDate=req.form['MaxDate'],
                                                   minDateHeight=req.form['MinDateHeight'], 
                                                   maxDateHeight=req.form['MaxDateHeight'], 
                                                   minDateWeight=req.form['MinDateWeight'], 
                                                   maxDateWeight=req.form['MaxDateWeight'])

            jsonInfo_medic=showingMedicationR(patientId, minDate=req.form['MinDate'], maxDate=req.form['MaxDate'])

            data=souper.find("tbody", id="Observation")
            createElem(souper, data, jsonInfo, ['Date', 'Display', 'Value'])

            souper.find("input", id="MinDate")["value"]=req.form['MinDate']
            souper.find("input", id="MaxDate")["value"]=req.form['MaxDate']
            souper.find("input", id="MinDateHeight")["value"]=req.form['MinDateHeight']
            souper.find("input", id="MaxDateHeight")["value"]=req.form['MaxDateHeight']
            souper.find("input", id="MinDateWeight")["value"]=req.form['MinDateWeight']
            souper.find("input", id="MaxDateWeight")["value"]=req.form['MaxDateWeight']

        else:
            jsonInfo=showingObservation(s, minDate=req.form['MinDate'],
                                           maxDate=req.form['MaxDate'],
                                           minDateHeight=req.form['MinDateHeight'], 
                                           maxDateHeight=req.form['MaxDateHeight'], 
                                           minDateWeight=req.form['MinDateWeight'], 
                                           maxDateWeight=req.form['MaxDateWeight'])

            jsonInfo_medic=showingMedicationR(s, minDate=req.form['MinDate'], maxDate=req.form['MaxDate'])

            patientId=s
            data=souper.find("tbody", id="Observation")
            createElem(souper, data, jsonInfo, ['Date', 'Display', 'Value', 'Component'])
            createElem(souper, med_data, jsonInfo_medic, ['Date', 'Status', 'Medication', 'Timing', 'dosageInstruction'])
            #data.string=f"http://localhost:8090/baseDstu3/Observation?patient.identifier={s}"
    
        return render_template_string(souper.prettify())

    else:
        jsonInfo=showing(all=1)
        createElem(souper, data, jsonInfo)
        try:
            os.remove("data_weight.csv")
        except:
            pass
        try:
            os.remove("data_height.csv")
        except:
            pass
        return render_template_string(souper.prettify())


@app.route('/data_height.csv', methods=['GET'])
def data():
    html_doc=open('./data_height.csv')
    souper=BeautifulSoup(html_doc, 'html.parser')
    return render_template_string(souper.prettify())

@app.route('/data_weight.csv', methods=['GET'])
def data_weight():
    html_doc=open('./data_weight.csv')
    souper=BeautifulSoup(html_doc, 'html.parser')
    return render_template_string(souper.prettify())


if __name__=='__main__':
    app.run()
