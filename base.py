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


#href=f"http://localhost:8090/baseDstu3/Observation?patient.identifier={y[x]}"
def createElem(doc, tab, elemList):
    print(tab)
    for y in elemList:
        trow = doc.new_tag("tr")
        tab.append(trow)
        for x in ['Name', 'Surname', 'Id']:
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
            data=souper.find("div", id="debug")
            data.string=f"http://localhost:8090/baseDstu3/Observation?patient.identifier={s}"

            #Telefon mi siadł, poczekaj chwilę
    
        return render_template_string(souper.prettify())

    else:
        jsonInfo=showing(all=1)
        createElem(souper, data, jsonInfo)

        return render_template_string(souper.prettify())


if __name__=='__main__':
    app.run()
