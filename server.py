from flask import Flask,redirect,jsonify,request ,Response
import requests
import json
from bs4 import BeautifulSoup
from flask_cors import CORS 
from collections import OrderedDict


app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return '<center><h1>Welcome to MSU_result scraper</h1></center>'

@app.route('/studentclass',methods=['POST','GET'])
def studClass():
    res = []

    data = request.get_json()

    RollNo = int(data['roll'])
    first = (RollNo//100)*100+1
    last = (RollNo//100)*100+48

    for roll in range(first,last+1):
        Stud = {}
        SubRes = {}
        RollNo = {'RegisterNo':roll}
        url = 'http://www.ugresult2023a.msuexamresult.in/print_result.php'
        # url = 'http://www.ugresult2020a.msuexamresult.in/print_result.php'
        response = requests.post(url,data=RollNo)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'html.parser')
            if(soup.find('noscript')):
                continue
            tables = soup.find('div', align="center")
            StudSection = tables.find_all('label')
            name = StudSection[1]
            name = name.get_text()
            Stud['Name'] = name
            Stud['Roll'] = roll
            course = StudSection[3]
            course = course.get_text()
            sub_row = tables.find_all('tr',style="height:25px;")
            for i in sub_row:
                d = i.find_all('td', align="center")
                Code = d[1].get_text().replace('&nbsp','').replace('\u00a0','')
                grade = d[2].get_text().replace('&nbsp','').replace('\u00a0','')
                SubRes[Code] = grade
            res.append(OrderedDict({**Stud , **SubRes}))
    json_response = json.dumps(res, ensure_ascii=False, indent=2)
    return Response(json_response, content_type='application/json;charset=utf-8')



@app.route('/classres',methods=['POST','GET'])
def classRes():
    res = []
    data = request.get_json()

    batch = data['batch']
    dept = data['dept']
    year = data['year']
    clg_code = data['clg_code']
    exam = data['exam']

    # return jsonify({
    #     'batch':batch,
    #     'dept':dept,
    #     'year':year,
    #     'clg_code':clg_code,
    #     'exam':exam
    # })

    def Url(batch,exam):
        if(batch == '2018'):
            if(exam == 'a'):
                return 'http://www.ugresult2018a.msuexamresult.in/print_result.php'
            else:
                return 'http://www.ugresult2018n.msuexamresult.in/print_result.php'
        elif(batch =='2019'):
            if(exam == 'a'):
                return 'http://www.ugresult2019a.msuexamresult.in/print_result.php'
            else:
                return 'http://www.ugresult2019n.msuexamresult.in/print_result.php'
        elif(batch == '2020'):
            if(exam == 'a'):
                return 'http://www.ugresult2020a.msuexamresult.in/print_result.php'
            else:
                return 'http://www.ugresult2020n.msuexamresult.in/print_result.php'
        elif(batch == '2021'):
            if(exam == 'a'):
                return 'http://www.ugresult2021a.msuexamresult.in/print_result.php'
            else:
                return 'http://www.ugresult2021n.msuexamresult.in/print_result.php'
        elif(batch == '2022'):
            if(exam == 'a'):
                return 'http://www.ugresult2022a.msuexamresult.in/print_result.php'
            else:
                return 'http://www.ugresult2020n.msuexamresult.in/print_result.php'
        elif(batch == '2023'):
            if(exam == 'a'):
                return 'http://www.ugresult2023a.msuexamresult.in/print_result.php'
            else:
                return 'http://www.ugresult2023n.msuexamresult.in/print_result.php'


    def dept_sel(dept):
        if(dept == 'mat'):
            return '1517'
        elif(dept == 'phy'):
            return '1522'
        elif(dept == 'che'):
            return '1505'
        elif(dept == 'eng'):
            return '1105'
        elif(dept == 'com'):
            return '1301'
        elif(dept == 'cs'):
            return '1506'
        else:
            return 0
        
    def year_sel(year,batch,exam):
        if (year == '1st' and batch == '2018' and exam=='n') or (year == '1st' and batch == '2019' and exam == 'a') or (year == '2nd' and batch == '2019' and exam == 'n') or (year == '2nd' and batch == '2020' and exam == 'a') or (year == '3rd' and batch == '2020' and exam == 'n') or (year == '3rd' and batch == '2021' and exam == 'a') :
            return '2018'
        elif (year == '1st' and batch == '2019' and exam=='n') or (year == '1st' and batch == '2020' and exam == 'a') or (year == '2nd' and batch == '2020' and exam == 'n') or (year == '2nd' and batch == '2021' and exam == 'a') or (year == '3rd' and batch == '2021' and exam == 'n') or (year == '3rd' and batch == '2022' and exam == 'a') :
            return '2019'
        elif (year == '1st' and batch == '2020' and exam=='n') or (year == '1st' and batch == '2021' and exam == 'a') or (year == '2nd' and batch == '2021' and exam == 'n') or (year == '2nd' and batch == '2022' and exam == 'a') or (year == '3rd' and batch == '2022' and exam == 'n') or (year == '3rd' and batch == '2023' and exam == 'a') :
            return '2020'
        elif (year == '1st' and batch == '2021' and exam=='n') or (year == '1st' and batch == '2022' and exam == 'a') or (year == '2nd' and batch == '2022' and exam == 'n') or (year == '2nd' and batch == '2023' and exam == 'a') or (year == '3rd' and batch == '2023' and exam == 'n') or (year == '3rd' and batch == '2024' and exam == 'a') :
            return '2021'
        elif (year == '1st' and batch == '2022' and exam=='n') or (year == '1st' and batch == '2023' and exam == 'a') or (year == '2nd' and batch == '2023' and exam == 'n') or (year == '2nd' and batch == '2024' and exam == 'a') or (year == '3rd' and batch == '2024' and exam == 'n') or (year == '3rd' and batch == '2025' and exam == 'a') :
            return '2022'
        else:
            return 0

    dept_code = dept_sel(dept)
    year_code = year_sel(year,batch,exam)
    start_code = '201'
    end_code = '248'

    Exam_URL = Url(batch,exam)

    first = year_code+clg_code+dept_code+start_code
    last = year_code+clg_code+dept_code+end_code
    first = int(first)
    last = int(last)


    for roll in range(first,last+1):
        Stud = {}
        SubRes = {}
        RollNo = {'RegisterNo':roll}
        # url = 'http://www.ugresult2021a.msuexamresult.in/index.php'
        response = requests.post(Exam_URL,data=RollNo)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'html.parser')
            if(soup.find('noscript')):
                continue
            tables = soup.find('div', align="center")
            StudSection = tables.find_all('label')
            name = StudSection[1]
            name = name.get_text()
            Stud['Name'] = name
            Stud['Roll'] = roll
            course = StudSection[3]
            course = course.get_text()
            sub_row = tables.find_all('tr',style="height:25px;")
            for i in sub_row:
                d = i.find_all('td', align="center")
                Code = d[1].get_text().replace('&nbsp','').replace('\u00a0','')
                grade = d[2].get_text().replace('&nbsp','').replace('\u00a0','')
                SubRes[Code] = grade
            res.append(OrderedDict({**Stud , **SubRes}))
    json_response = json.dumps(res, ensure_ascii=False, indent=2)
    return Response(json_response, content_type='application/json;charset=utf-8')


@app.route('/student',methods=['POST','GET'])
def studRes():
    result = []
    studDetails = {}
    SubRes = {}
    data = request.get_json()
    roll = data['roll']   
    # roll = '20201311506237'
    RollNo = {'RegisterNo':roll}
    url = 'http://www.ugresult2023a.msuexamresult.in/print_result.php'

    response = requests.post(url,data=RollNo)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'html.parser')
        if(soup.find('noscript')):
            result.append('<p>Invalid Roll Number... Please check the roll number...</p>')
        r = soup.find('div', align="center")
        res_container = r.find('table', style="width:790px; height:100%;")
        studInfo = res_container.find_all('label')
        name = studInfo[1].get_text()
        rollno = studInfo[0].get_text().replace('\r\n','')
        studDetails.update({'Name':name,'Roll':rollno})

        res_table = res_container.find('table',width="100%",border="1",cellpadding="0");
        res_row = res_table.find_all('tr',style="height:25px;")
        for i in res_row:
            res_data = i.find_all('td', align="center")
            subj = res_data
            Code = subj[1].get_text().replace('&nbsp','').replace('\u00a0','')
            grade = subj[2].get_text().replace('&nbsp','').replace('\u00a0','')
            SubRes[Code] = grade
        result.append(studDetails)
        result.append(SubRes)
    return jsonify(result)



# if __name__ == '__main__':
#     app.run(debug=True)         