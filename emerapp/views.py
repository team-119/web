from emerapp.models import Patient
from emerapp.forms import PatientForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests
import re
import json
from bs4 import BeautifulSoup as bs

def home(request):  
    return render(request, 'emerapp/home.html')
    
def user_input(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid(): #유효성 검사
            patient_id = form.save() #여기에 저장
            return redirect('/user_output/{}'.format(patient_id))
        
        else:
            print(form.errors)
            return HttpResponse("failed") #유효성 검사 실패
    else:
        form = PatientForm() #post 요청 안 들어옴 
    return render(request, 'emerapp/user_input.html', {'form': form}) #유저인풋.html 소환 

def hos_input(request):
    if 'hos' in request.GET:
        hos = request.GET['hos']
        patients = Patient.objects.filter(hos = hos)
    else:
        patients = Patient.objects.all()
    if request.method == 'POST':
        hos = request.POST['hos']
        patients = Patient.objects.filter(hos = hos)
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_id = form.save()
            return redirect('/user_output/{}'.format(patient_id))
        else:
            print(form.errors)
            return HttpResponse("failed")
    else:
        form = PatientForm()
    return render(request, 'emerapp/hos_input.html', {'form': form, 'patients': patients})
 
    
#####################################################################################################################################################################################################################################################################################################################################################################


def user_output(request, patient_id):
    url = "http://portal.nemc.or.kr/medi_info/dashboards/dash_total_emer_org_popup_for_egen.do?&juso=&lon=&lat=&con=on&emogloca=21&emogdstr=2138&asort=A&asort=C&asort=D&rltmCd=O001&rltmCd=O002&rltmCd=O003&rltmCd=O004&rltmCd=O048&rltmCd=O049&rltmCd=O046&rltmCd=O047&rltmCd=O005&rltmCd=O019&rltmCd=O010&rltmCd=O020&rltmCd=O017&rltmCd=O006&rltmCd=O007&rltmCd=O009&rltmCd=O015&rltmCd=O011&rltmCd=O012&rltmCd=O016&rltmCd=O008&rltmCd=O014&rltmCd=O013&rltmCd=O018&rltmCd=O038&rltmCd=O025&rltmCd=O021&rltmCd=O024&rltmCd=O022&rltmCd=O023&rltmCd=O026&rltmCd=O036&rltmCd=O030&rltmCd=O031&rltmCd=O032&rltmCd=O033&rltmCd=O034&rltmCd=O035&rltmCd=O037&rltmCd=O027&rltmCd=O028&rltmCd=O029&svdssCd=Y0010&svdssCd=Y0020&svdssCd=Y0031&svdssCd=Y0032&svdssCd=Y0041&svdssCd=Y0042&svdssCd=Y0051&svdssCd=Y0052&svdssCd=Y0060&svdssCd=Y0070&svdssCd=Y0131&svdssCd=Y0132&svdssCd=Y0081&svdssCd=Y0082&svdssCd=Y0091&svdssCd=Y0092&svdssCd=Y0111&svdssCd=Y0112&svdssCd=Y0113&svdssCd=Y0160&svdssCd=Y0141&svdssCd=Y0142&svdssCd=Y0171&svdssCd=Y0172&svdssCd=Y0150&svdssCd=Y0120&svdssCd=Y0100&afterSearch=map&theme=BLACK&refreshTime=60&spreadAllMsg=allClose"
    response = requests.get(url)
    html = response.text
    soup = bs(html,"html.parser")
    
    number = soup.find_all('div', class_="data_data data_td_O038") # 일반 병상 
    
    n = 0
    for i in number:
        number[n] = re.compile('\w+').findall(i.get_text()) 
        print(re.compile('\w+').findall(i.get_text()))
        n+=1
    #number 안에 병원별로 [사용된 병상, 전체 병상 수] 들어가있다 
    
    name_hos = [] #병원 이름
    name_sur = [] #수술 이름
    sungmo_sur = [-1] #병원별 수술 가능여부(1번째 칸부터 수술1)
    chu_sur = [-1]
    #t0 = [Patient.objects.filter(id = patient_id).values('ETA_S')[0]['ETA_S'], Patient.objects.filter(id = patient_id).values('ETA_U')[0]['ETA_U'], Patient.objects.filter(id = patient_id).values('ETA_B')[0]['ETA_B'],Patient.objects.filter(id = patient_id).values('ETA_C')[0]['ETA_C']] # 병원별 도착 시간
    
    #print("time is  ===== ",Patient.objects.filter(id = patient_id).values('ETA_S')[0]['ETA_S'])
    
    
    #정렬 함수 정의
    def qsort(a):
        if len(a) <= 1:
            return a
        p = a[len(a) // 2]
        al = []
        ae = []
        ar = []
        for i in a:
            if i < p:
                al.append(i)
            elif i > p:
                ar.append(i)
            else:
                ae.append(i)
        return qsort(al) + ae + qsort(ar)

    # 병원 이름     
    name_hos = soup.find_all('div',class_ = "dash_box")
    n = 0
    for i in name_hos:
        name_hos[n] = i['data-emogdesc']
        n+=1
    print(name_hos)
    
    # 수술종류 이름 
    sur1 = soup.find_all('div',class_ = 'data_header')
    sur2 = soup.find_all('td')
    n = 0
    for i in sur1[42:69]:
        #print(i.get_text())
        name_sur.append(i.get_text())
        n+=1
    #성모 : [130:156] / 추병원 : [284:310]

    # sur_hos는 수술실리스트 집합
    s1_1 = [[1,[2,2],[4,4]]] # 성모,수술종류_응급도
    s1_2 = [[1,[4,4],[11,11]]]
    s1_3 = [[1,[12,12],[14,14]]]
    s2_1 = [[1,[2,2],[4,4]]]
    s2_2 = [[1,[4,4],[11,11]]]
    s2_3 = [[1,[12,12],[14,14]]]
    s3_1 = [[1,[2,2],[4,4]]]
    s3_2 = [[1,[4,4],[11,11]]]
    s3_3 = [[1,[12,12],[14,14]]]
    s4_1 = [[1,[2,2],[4,4]]]
    s4_2 = [[1,[4,4],[11,11]]]
    s4_3 = [[1,[12,12],[14,14]]]
    s5_1 = [[1,[2,2],[4,4]]]
    s5_2 = [[1,[4,4],[11,11]]]
    s5_3 = [[1,[12,12],[14,14]]]
    s6_1 = [[1,[2,2],[4,4]]]
    s6_2 = [[1,[4,4],[11,11]]]
    s6_3 = [[1,[12,12],[14,14]]]
    s7_1 = [[1,[2,2],[4,4]]]
    s7_2 = [[1,[4,4],[11,11]]]
    s7_3 = [[1,[12,12],[14,14]]]
    s8_1 = [[1,[2,2],[4,4]]]
    s8_2 = [[1,[4,4],[11,11]]]
    s8_3 = [[1,[12,12],[14,14]]]
    s9_1 = [[1,[2,2],[4,4]]]
    s9_2 = [[1,[4,4],[11,11]]]
    s9_3 = [[1,[12,12],[14,14]]]
    s10_1 = [[1,[2,2],[4,4]]]
    s10_2 = [[1,[4,4],[11,11]]]
    s10_3 = [[1,[12,12],[14,14]]]
    s11_1 = [[1,[2,2],[4,4]]]
    s11_2 = [[1,[4,4],[11,11]]]
    s11_3 = [[1,[12,12],[14,14]]]
    s12_1 = [[1,[2,2],[4,4]]]
    s12_2 = [[1,[4,4],[11,11]]]
    s12_3 = [[1,[12,12],[14,14]]]
    s13_1 = [[1,[2,2],[4,4]]]
    s13_2 = [[1,[4,4],[11,11]]]
    s13_3 = [[1,[12,12],[14,14]]]
    s14_1 = [[1,[2,2],[4,4]]]
    s14_2 = [[1,[4,4],[11,11]]]
    s14_3 = [[1,[12,12],[14,14]]]
    s15_1 = [[1,[2,2],[4,4]]]
    s15_2 = [[1,[4,4],[11,11]]]
    s15_3 = [[1,[12,12],[14,14]]]
    s16_1 = [[1,[2,2],[4,4]]]
    s16_2 = [[1,[4,4],[11,11]]]
    s16_3 = [[1,[12,12],[14,14]]]
    s17_1 = [[1,[2,2],[4,4]]]
    s17_2 = [[1,[4,4],[11,11]]]
    s17_3 = [[1,[12,12],[14,14]]]
    s18_1 = [[1,[2,2],[4,4]]]
    s18_2 = [[1,[4,4],[11,11]]]
    s18_3 = [[1,[12,12],[14,14]]]
    s19_1 = [[1,[2,2],[4,4]]]
    s19_2 = [[1,[4,4],[11,11]]]
    s19_3 = [[1,[12,12],[14,14]]]
    s20_1 = [[1,[2,2],[4,4]]]
    s20_2 = [[1,[4,4],[11,11]]]
    s20_3 = [[1,[12,12],[14,14]]]
    s21_1 = [[1,[2,2],[4,4]]]
    s21_2 = [[1,[4,4],[11,11]]]
    s21_3 = [[1,[12,12],[14,14]]]
    s22_1 = [[1,[2,2],[4,4]]]
    s22_2 = [[1,[4,4],[11,11]]]
    s22_3 = [[1,[12,12],[14,14]]]
    s23_1 = [[1,[2,2],[4,4]]]
    s23_2 = [[1,[4,4],[11,11]]]
    s23_3 = [[1,[12,12],[14,14]]]
    s24_1 = [[1,[2,2],[4,4]]]
    s24_2 = [[1,[4,4],[11,11]]]
    s24_3 = [[1,[12,12],[14,14]]]
    s25_1 = [[1,[2,2],[4,4]]]
    s25_2 = [[1,[4,4],[11,11]]]
    s25_3 = [[1,[12,12],[14,14]]]
    s26_1 = [[1,[2,2],[4,4]]]
    s26_2 = [[1,[4,4],[11,11]]]
    s26_3 = [[1,[12,12],[14,14]]]
    s27_1 = [[1,[2,2],[4,4]]]
    s27_2 = [[1,[4,4],[11,11]]]
    s27_3 = [[1,[12,12],[14,14]]]


    c1_1 = [[1, [1, 1], [3, 3]]]
    c1_2 = [[2, [5, 5], [12, 12]]]
    c1_3 = [[3, [13, 13], [15, 15]]]
    c2_1 = [[1, [1, 1], [3, 3]]]
    c2_2 = [[2, [5, 5], [12, 12]]]
    c2_3 = [[3, [13, 13], [15, 15]]]
    c3_1 = [[1, [1, 1], [3, 3]]]
    c3_2 = [[2, [5, 5], [12, 12]]]
    c3_3 = [[3, [13, 13], [15, 15]]]
    c4_1 = [[1, [1, 1], [3, 3]]]
    c4_2 = [[2, [5, 5], [12, 12]]]
    c4_3 = [[3, [13, 13], [15, 15]]]
    c5_1 = [[1, [1, 1], [3, 3]]]
    c5_2 = [[2, [5, 5], [12, 12]]]
    c5_3 = [[3, [13, 13], [15, 15]]]
    c6_1 = [[1, [1, 1], [3, 3]]]
    c6_2 = [[2, [5, 5], [12, 12]]]
    c6_3 = [[3, [13, 13], [15, 15]]]
    c7_1 = [[1, [1, 1], [3, 3]]]
    c7_2 = [[2, [5, 5], [12, 12]]]
    c7_3 = [[3, [13, 13], [15, 15]]]
    c8_1 = [[1, [1, 1], [3, 3]]]
    c8_2 = [[2, [5, 5], [12, 12]]]
    c8_3 = [[3, [13, 13], [15, 15]]]
    c9_1 = [[1, [1, 1], [3, 3]]]
    c9_2 = [[2, [5, 5], [12, 12]]]
    c9_3 = [[3, [13, 13], [15, 15]]]
    c10_1 = [[1, [1, 1], [3, 3]]]
    c10_2 = [[2, [5, 5], [12, 12]]]
    c10_3 = [[3, [13, 13], [15, 15]]]
    c11_1 = [[1, [1, 1], [3, 3]]]
    c11_2 = [[2, [5, 5], [12, 12]]]
    c11_3 = [[3, [13, 13], [15, 15]]]
    c12_1 = [[1, [1, 1], [3, 3]]]
    c12_2 = [[2, [5, 5], [12, 12]]]
    c12_3 = [[3, [13, 13], [15, 15]]]
    c13_1 = [[1, [1, 1], [3, 3]]]
    c13_2 = [[2, [5, 5], [12, 12]]]
    c13_3 = [[3, [13, 13], [15, 15]]]
    c14_1 = [[1, [1, 1], [3, 3]]]
    c14_2 = [[2, [5, 5], [12, 12]]]
    c14_3 = [[3, [13, 13], [15, 15]]]
    c15_1 = [[1, [1, 1], [3, 3]]]
    c15_2 = [[2, [5, 5], [12, 12]]]
    c15_3 = [[3, [13, 13], [15, 15]]]
    c16_1 = [[1, [1, 1], [3, 3]]]
    c16_2 = [[2, [5, 5], [12, 12]]]
    c16_3 = [[3, [13, 13], [15, 15]]]
    c17_1 = [[1, [1, 1], [3, 3]]]
    c17_2 = [[2, [5, 5], [12, 12]]]
    c17_3 = [[3, [13, 13], [15, 15]]]
    c18_1 = [[1, [1, 1], [3, 3]]]
    c18_2 = [[2, [5, 5], [12, 12]]]
    c18_3 = [[3, [13, 13], [15, 15]]]
    c19_1 = [[1, [1, 1], [3, 3]]]
    c19_2 = [[2, [5, 5], [12, 12]]]
    c19_3 = [[3, [13, 13], [15, 15]]]
    c20_1 = [[1, [1, 1], [3, 3]]]
    c20_2 = [[2, [5, 5], [12, 12]]]
    c20_3 = [[3, [13, 13], [15, 15]]]
    c21_1 = [[1, [1, 1], [3, 3]]]
    c21_2 = [[2, [5, 5], [12, 12]]]
    c21_3 = [[3, [13, 13], [15, 15]]]
    c22_1 = [[1, [1, 1], [3, 3]]]
    c22_2 = [[2, [5, 5], [12, 12]]]
    c22_3 = [[3, [13, 13], [15, 15]]]
    c23_1 = [[1, [1, 1], [3, 3]]]
    c23_2 = [[2, [5, 5], [12, 12]]]
    c23_3 = [[3, [13, 13], [15, 15]]]
    c24_1 = [[1, [1, 1], [3, 3]]]
    c24_2 = [[2, [5, 5], [12, 12]]]
    c24_3 = [[3, [13, 13], [15, 15]]]
    c25_1 = [[1, [1, 1], [3, 3]]]
    c25_2 = [[2, [5, 5], [12, 12]]]
    c25_3 = [[3, [13, 13], [15, 15]]]
    c26_1 = [[1, [1, 1], [3, 3]]]
    c26_2 = [[2, [5, 5], [12, 12]]]
    c26_3 = [[3, [13, 13], [15, 15]]]
    c27_1 = [[1, [1, 1], [3, 3]]]
    c27_2 = [[2, [5, 5], [12, 12]]]
    c27_3 = [[3, [13, 13], [15, 15]]]
    sur_hos = [[ s1_1,s1_2,s1_3,c1_1,c1_2,c1_3 ] ,[ s2_1,s2_2,s2_3,c2_1,c2_2,c2_3 ] ,[ s3_1,s3_2,s3_3,c3_1,c3_2,c3_3 ] ,[ s4_1,s4_2,s4_3,c4_1,c4_2,c4_3 ] ,[ s5_1,s5_2,s5_3,c5_1,c5_2,c5_3 ] ,[ s6_1,s6_2,s6_3,c6_1,c6_2,c6_3 ] ,[ s7_1,s7_2,s7_3,c7_1,c7_2,c7_3 ] ,[ s8_1,s8_2,s8_3,c8_1,c8_2,c8_3 ] ,[ s9_1,s9_2,s9_3,c9_1,c9_2,c9_3 ] ,[ s10_1,s10_2,s10_3,c10_1,c10_2,c10_3 ] ,[ s11_1,s11_2,s11_3,c11_1,c11_2,c11_3 ] ,[ s12_1,s12_2,s12_3,c12_1,c12_2,c12_3 ] ,[ s13_1,s13_2,s13_3,c13_1,c13_2,c13_3 ] ,[ s14_1,s14_2,s14_3,c14_1,c14_2,c14_3 ] ,[ s15_1,s15_2,s15_3,c15_1,c15_2,c15_3 ] ,[ s16_1,s16_2,s16_3,c16_1,c16_2,c16_3 ] ,[ s17_1,s17_2,s17_3,c17_1,c17_2,c17_3 ] ,[ s18_1,s18_2,s18_3,c18_1,c18_2,c18_3 ] ,[ s19_1,s19_2,s19_3,c19_1,c19_2,c19_3 ] ,[ s20_1,s20_2,s20_3,c20_1,c20_2,c20_3 ] ,[ s21_1,s21_2,s21_3,c21_1,c21_2,c21_3 ] ,[ s22_1,s22_2,s22_3,c22_1,c22_2,c22_3 ] ,[ s23_1,s23_2,s23_3,c23_1,c23_2,c23_3 ] ,[ s24_1,s24_2,s24_3,c24_1,c24_2,c24_3 ] ,[ s25_1,s25_2,s25_3,c25_1,c25_2,c25_3 ] ,[ s26_1,s26_2,s26_3,c26_1,c26_2,c26_3 ] ,[ s27_1,s27_2,s27_3,c27_1,c27_2,c27_3 ]]
    stay = [[1,3],[1,5],[0,7],[1,9],[0,11],[1,13],[1,15],[1,17],[1,19],[1,21],[1,23],[2,25],[1,27],[2,30],[1,33],[3,36],[1,23],[1,42],[2,45],[1,48],[0,51],[1,54],[1,57],[0,60],[1,62],[0,64],[1,66],[0,68]] #병상 체류시간
 
    #제일 큰 조건문은 빼야됨
    #직접 온 사람일때 db 업데이트 (by = 1)
    #병원 입력창에서 받고 난 후에 하는 연산
        
    if Patient.objects.filter(id = patient_id).values('by')[0]['by'] == 1: #병원 직접 
        t0 = [[0,0],[0,0],[0,0],[0,0]] # 병원별 도착 시간
        tfinal = [] #이 경우에는 도착 = 치료시작
        t = ['a','a','a','a']
        t[0] = Patient.objects.filter(id = patient_id).values('ETA_S')[0]['ETA_S']
        t[1] = Patient.objects.filter(id = patient_id).values('ETA_U')[0]['ETA_U']
        t[2] = Patient.objects.filter(id = patient_id).values('ETA_B')[0]['ETA_B']
        t[3] = Patient.objects.filter(id = patient_id).values('ETA_C')[0]['ETA_C']
        
        for i in range(0,4): #ETA 존재하면 이미 간 병원 
            if t[i] != '-':
                tfinal.append(int(t[i].split(':')[0]))
                tfinal.append(int(t[i].split(':')[1]))
                tfinal.append(i) #사실 이때 i가 hos
                
        #수술실 타임라인 가져오기
        #지금 있는거보다 더 많으면 가져오기
        print("111111111111111111111111")
        # = Patient.objects.latest('id')
        hos = Patient.objects.filter(id = patient_id).values('hos')[0]['hos']
        sur = Patient.objects.filter(id = patient_id).values('oper')[0]['oper']
        emer = Patient.objects.filter(id = patient_id).values('emer')[0]['emer']
        
        def tplus(a,b,c,d): #시간 연산 알고리즘()
            if b+d >=60:
                if a+c >=24:
                    return [a+c-23,b+d-60]
                else:
                    return [a+c+1,b+d-60]
            else:
                if a+c >=24:
                    return [a+c-24,b+d]
                else:
                    return [a+c,b+d]
        
        def tcom(a,b,c,d):
            if a > c: #앞이 더 큼
                return 1 #더 빠른거
            elif a == c:
                if b > d:
                    return 1
                elif b == d:
                    return 2 #같으면 2
                else:
                    return 0
            else:
                return 0
            
        def tmin(a,b,c,d): #시간 뺄셈 알고리즘()
            if tplus(a,b,c,d) == 2:
                return "false"
            else: #앞 시간이 클때 
                if b >= d: # 무조건 a >= c
                    return [a-c,b-d]
                else: #무조건 a > c 
                    return [a-c-1,b-d+60]
            
        def timeon(a,b):
            return "a"+":"+"b"
        
        #tfinal = [시, 분, 병원]
        #db 미는 부분 추가 
 
        if sur != 0: #수술 필요시
            if hos == '0': #성모 병원 간 사람
         
                if tcom(sur_hos[sur-1][emer-1][-1][2][0],sur_hos[sur-1][emer-1][-1][2][1],t0[0][0],t0[0][1]) == 1 or 2: #도착하자마자 가능 
                    tfinal.append([t0[0][0],t0[0][1],0])
                else: #기다려야됨
                    tfinal.append([sur_hos[sur-1][emer-1][-1][2][0],sur_hos[sur-1][emer-1][-1][2][1],0])
                sur_hos[sur-1][emer-1].append([patient_id,[tfinal[0],tfinal[1]],tplus(tfinal[0],tfinal[1],stay[sur][0],stay[sur][1])])
      
            elif hos == '3': #추병원 간 사람
           
                if tcom(sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1],t0[3][0],t0[3][1]) == 1 or 2: #도착하자마자 가능
                    tfinal.append([t0[3][0],t0[3][1],3])
                else: #기다려야됨
                    tfinal.append([sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1],3])
                sur_hos[sur-1][emer+2].append([patient_id,[tfinal[0],tfinal[1]],tplus(tfinal[0],tfinal[1],stay[sur][0],stay[sur][1])])
        
        #타임라인 업데이트
        gaptime = [0,0]
        if emer == 3: #응급도 클수록 우선 
            if tcom(sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1]) == 1 or 2 : #도착 시간이 더 늦어서 변동X
                gaptime = [0,0]
            else:
                gaptime = tmin(sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1])
                for i in sur_hos[sur-1][emer-2+tfinal[0][2]]: 
                    i[1] = tplus(i[1][0],i[1][1],gaptime[0],gaptime[1])
                    i[2] = tplus(i[2][0],i[2][1],gaptime[0],gaptime[1])
 
            if tcom(sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][1],sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][1]) == 1 or 2: #도착 시간이 더 늦어서 변동X
                gaptime = [0,0]
            else:
                gaptime = tmin(sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][1],sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][1])
                for i in sur_hos[sur-1][emer-3+tfinal[0][2]]:
                    i[1] = tplus(i[1][0],i[1][1],gaptime[0],gaptime[1])
                    i[2] = tplus(i[2][0],i[2][1],gaptime[0],gaptime[1])
 
        elif emer == 2:
            if tcom(sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1]) == 1 or 2: #도착 시간이 더 늦어서 변동X
                gaptime = [0,0]
            else :
                gaptime = tmin(sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1])
                for i in sur_hos[sur-1][emer-2+tfinal[0][2]]:
                    i[1] = tplus(i[1][0],i[1][1],gaptime[0],gaptime[1])
                    i[2] = tplus(i[2][0],i[2][1],gaptime[0],gaptime[1])
 
    
        if sur !=0 :
            Patient.objects.filter(id = patient_id).update(hos = str(tfinal[0][2]), start = timeon(tfinal[0][0],tfinal[0][1]), end = timeon(sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1]))
        else:
            Patient.objects.filter(id = patient_id).update(hos = str(tfinal[0][2]), start = timeon(tfinal[0][0],tfinal[0][1]), end = timeon(tfinal[0][0],tfinal[0][1]))
        
        hos = Patient.objects.filter(id = patient_id).values('hos')[0]['hos']
        print(hos)
        return redirect('/hos_input?hos={}'.format(hos))
            
#구급차로 직접 이송한 환자
    elif Patient.objects.filter(id = patient_id).values('by')[0]['by'] == 0: #구급차로 이동 
        
        #t0 받아오는 코드
        t0 = [[0,0],[0,0],[0,0],[0,0]] # 병원별 도착 시간
        t = ['a','a','a','a']
        t[0] = Patient.objects.filter(id = patient_id).values('ETA_S')[0]['ETA_S']
        t[1] = Patient.objects.filter(id = patient_id).values('ETA_U')[0]['ETA_U']
        t[2] = Patient.objects.filter(id = patient_id).values('ETA_B')[0]['ETA_B']
        t[3] = Patient.objects.filter(id = patient_id).values('ETA_C')[0]['ETA_C']
     
        n = 0
        for i in t:
            t0[n][0] = int(i.split(':')[0])
            t0[n][1] = int(i.split(':')[1])
            print(t0[n])
            n+=1
     
        def tplus(a,b,c,d): #시간 덧셈 알고리즘()
            if b+d >=60:
                if a+c >=24:
                    return [a+c-23,b+d-60]
                else:
                    return [a+c+1,b+d-60]
            else:
                if a+c >=24:
                    return [a+c-24,b+d]
                else:
                    return [a+c,b+d] 
            n = 0
            for i in t:
                t0[n] = i.split(':')
                n+=1
       
        def tmin(a,b,c,d): #시간 뺄셈 알고리즘()
            if tplus(a,b,c,d) == 2:
                return "false"
            else: #앞 시간이 클때 
                if b >= d: # 무조건 a >= c
                    return [a-c,b-d]
                else: #무조건 a > c 
                    return [a-c-1,b-d+60]
                    
        def tcom(a,b,c,d):
                if a > c: #앞이 더 큼
                    return 1 #더 빠른거
                elif a == c:
                    if b > d:
                        return 1
                    elif b == d:
                        return 2 #같으면 2
                    else:
                        return 0
                else:
                    return 0
     
        def timeon(a,b):
            return str(a)+":"+str(b)
     
        # 체크리스트에서 sur,emer 받아오기
        emer = Patient.objects.filter(id = patient_id).values('emer')[0]['emer']
        sur = Patient.objects.filter(id = patient_id).values('oper')[0]['oper']
     
        #병상 정보 크롤링 [사용된 병상, 전체 병상 수]
        number = soup.find_all('div',class_="data_data data_td_O038") # 일반 병상
        n = 0
        for i in number:
            number[n] = re.compile('\w+').findall(i.get_text())
            n+=1
               # 치료 가능 여부 [불가능, 가능, 미제공]
            sur2 = soup.find_all('td')
          
        n = 0 
        for i in sur2:
            sur2[n] = re.compile('\w+').findall(i.get_text())
            n+=1
          
        n = 0
        for i in sur2[129:156]:
            n+=1 # 칸 번호 = 수술 종류 (1부터 시작)
            if i[-1] == "가능":
                sungmo_sur.append(1)
            elif i[-1] == "불가능":
                sungmo_sur.append(0)
            else:
                sungmo_sur.append(2)
         
        n = 0
        for i in sur2[283:310]:
            n+=1 # 칸 번호 = 수술 종류 (1부터 시작)
         
            if i[-1] == "가능":
                chu_sur.append(1)
            elif i[-1] == "불가능":
                chu_sur.append(0)
            else:
                chu_sur.append(2)
         
            
            
        #가능한 병원 찾기 
         
        tfinal = [] #최종 치료 가능 시작 시간
        poss_hos = [-1,-1,-1,-1]  #가능한 병원(병원순서대로 칸 번호)
           
        if sur == 0: #중증X -> 응급실 유무만
            n = 0
            for i in number:
                if int(i[0]) < int(i[1]): #병상 있으면 가능(1)
                    poss_hos[n] = 1
                    tfinal.append([t0[n][0],t0[n][1],n]) #가능하면 [[t0(시,분)),병원숫자](가까운데로)
                else: #없으면 불가능(0)
                    poss_hos[n] = 0
                n+=1
            
            #이때는 바로 tfinal sort로 넘어가면 됨
            tfinal = qsort(tfinal)
            
            result = {}
            result['emer'] = emer
            result['oper'] = sur
            result['hos'] = str(tfinal[0][2])
            result['time'] = Patient.objects.filter(id = patient_id).values('time')[0]['time']
            result['ETE_S'] = int(Patient.objects.filter(id = patient_id).values('ETE_S')[0]['ETE_S'])
            result['ETE_U'] = int(Patient.objects.filter(id = patient_id).values('ETE_U')[0]['ETE_U'])
            result['ETE_B'] = int(Patient.objects.filter(id = patient_id).values('ETE_B')[0]['ETE_B'])
            result['ETE_C'] = int(Patient.objects.filter(id = patient_id).values('ETE_C')[0]['ETE_C'])
            result['ETA_S'] = t0[0]
            result['ETA_U'] = t0[1]
            result['ETA_B'] = t0[2]
            result['ETA_C'] = t0[3]
            result['start'] = timeon(tfinal[0][0],tfinal[0][1])
            result['end'] = timeon(tfinal[0][0],tfinal[0][1])
            
            #db 업데이트
            Patient.objects.filter(id = patient_id).update(hos = str(tfinal[0][2]), start = timeon(tfinal[0][0],tfinal[0][1]), end = timeon(sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1]))
    
    
        else: #(poss_hos에 병원 2개) (성모,추)
            n = 0
            if sungmo_sur[sur] == 1:
                poss_hos[0] = 3 #성모 가능
            
            elif sungmo_sur[sur] == 0 or 2:
                poss_hos[0] = 2 #성모 불가능
              
            if chu_sur[sur] == 1:
                poss_hos[3] = 3 #추 가능  
          
            elif chu_sur[sur] == 0 or 2:
                poss_hos[3] = 2 #추 불가능
            n+=1
    
            #병원 별로 도착시간과 같은 응급도 타임라인에서 마지막 치료종료시간과 비교 
            if poss_hos[0] == 3: #0,3 => 성모 가능
                if  tcom(sur_hos[sur-1][emer-1][-1][2][0],sur_hos[sur-1][emer-1][-1][2][1],t0[0][0],t0[0][1]) == 1 or 2: #도착하자마자 가능
                    tfinal.append([t0[0][0],t0[0][1],0])
                else: #기다려야됨
                    tfinal.append([sur_hos[sur-1][emer-1][-1][2][0],sur_hos[sur-1][emer-1][-1][2][1],0])
    
            if poss_hos[3] == 3: #3,3 => 추 가능
                if tcom(sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1],t0[3][0],t0[3][1]) == 1 or 2: #종료시간과 도착 시간 비교
                    tfinal.append([t0[3][0],t0[3][1],3])
                else:
                    tfinal.append([sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1],3])
    
            result = {}
            if tfinal == []: #둘다 불가능 할때(거리순)
                if tcom(t0[0][0],t0[0][1],t0[3][0],t0[3][1]) == 1 or 2: #추병원이 더 가깝다
                    tfinal.append([t0[3][0],t0[3][1],3])
                    result['emer'] = emer
                    result['oper'] = sur
                    result['hos'] = "3"
                    result['time'] = Patient.objects.filter(id = patient_id).values('time')[0]['time']
                    result['ETE_S'] = int(Patient.objects.filter(id = patient_id).values('ETE_S')[0]['ETE_S'])
                    result['ETE_U'] = int(Patient.objects.filter(id = patient_id).values('ETE_U')[0]['ETE_U'])
                    result['ETE_B'] = int(Patient.objects.filter(id = patient_id).values('ETE_B')[0]['ETE_B'])
                    result['ETE_C'] = int(Patient.objects.filter(id = patient_id).values('ETE_C')[0]['ETE_C'])
                    result['ETA_S'] = t0[0]
                    result['ETA_U'] = t0[1]
                    result['ETA_B'] = t0[2]
                    result['ETA_C'] = t0[3]
                    result['poss'] = 1
                    
                else:
                    tfinal.append([t0[0][0],t0[0][1],0])
                    result['emer'] = emer
                    result['oper'] = sur
                    result['hos'] = "0"
                    result['time'] = Patient.objects.filter(id = patient_id).values('time')[0]['time']
                    result['ETE_S'] = int(Patient.objects.filter(id = patient_id).values('ETE_S')[0]['ETE_S'])
                    result['ETE_U'] = int(Patient.objects.filter(id = patient_id).values('ETE_U')[0]['ETE_U'])
                    result['ETE_B'] = int(Patient.objects.filter(id = patient_id).values('ETE_B')[0]['ETE_B'])
                    result['ETE_C'] = int(Patient.objects.filter(id = patient_id).values('ETE_C')[0]['ETE_C'])
                    result['ETA_S'] = t[0]
                    result['ETA_U'] = t[1]
                    result['ETA_B'] = t[2]
                    result['ETA_C'] = t[3]
                    result['poss'] = 1
    
                if sur == 0 :
                    Patient.objects.filter(id = patient_id).update(hos = str(tfinal[0][2]), start = timeon(tfinal[0][0],tfinal[0][1]), end = timeon(sur_hos[sur-1][emer+2][-1][2][0],sur_hos[sur-1][emer+2][-1][2][1]))
                
                else :
                    Patient.objects.filter(id = patient_id).update(hos = str(tfinal[0][2]), start = timeon(tfinal[0][0],tfinal[0][1]), end = timeon(tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])[0],tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])[1]))
    
            else: #수술 가능 병원 존재 
                #tfinal 정렬
                tfinal = qsort(tfinal)
     
                #환자, 타임라인 업데이트
                #patient_list.extend([patient_id,tfinal[0][1],tfinal[0][0],tfinal[0][0]+stay[sur]]) # 정한 병원, tfinal, 예상 완료시간
                if sur != 0:
                    sur_hos[sur-1][emer-1+tfinal[0][2]].append([patient_id,[tfinal[0][0],tfinal[0][1]],tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])]) #0 emer-1 / 3 emer+2
     
                #응급도별 타임라인 시간 조정 (1일때는 변화 X)
                gaptime = [0,0]
                if emer == 3: #응급도 클수록 우선
                    if tcom(sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1]) == 1 or 2 : #도착 시간이 더 늦어서 변동X
                        gaptime = [0,0]
                    else:
                        gaptime = tmin(sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1])
                        for i in sur_hos[sur-1][emer-2+tfinal[0][2]]: 
                            i[1] = tplus(i[1][0],i[1][1],gaptime[0],gaptime[1])
                            i[2] = tplus(i[2][0],i[2][1],gaptime[0],gaptime[1])
     
                    if tcom(sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][1],sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][1]): #도착 시간이 더 늦어서 변동X
                        gaptime = [0,0]
                    else:
                        gaptime = tmin(sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-2+tfinal[0][2]][-1][2][1],sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-3+tfinal[0][2]][0][1][1])
                        for i in sur_hos[sur-1][emer-3+tfinal[0][2]]:
                            i[1] = tplus(i[1][0],i[1][1],gaptime[0],gaptime[1])
                            i[2] = tplus(i[2][0],i[2][1],gaptime[0],gaptime[1])
     
                elif emer == 2:
                    if tcom(sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1]): #도착 시간이 더 늦어서 변동X
                        gaptime = [0,0]
                    else :
                        gaptime = tmin(sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][0],sur_hos[sur-1][emer-1+tfinal[0][2]][-1][2][1],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][0],sur_hos[sur-1][emer-2+tfinal[0][2]][0][1][1])
                        for i in sur_hos[sur-1][emer-2+tfinal[0][2]]:
                            i[1] = tplus(i[1][0],i[1][1],gaptime[0],gaptime[1])
                            i[2] = tplus(i[2][0],i[2][1],gaptime[0],gaptime[1])
     
                result = {} #출력할 결과물
                #출력 / 필드명 : emer, oper, hos, by, time(현재시간), ETE_S, ETE_U, ETE_B, ETE_C, ETA_S, ETA_U, ETA_B, ETA_C, start, end 를 딕셔너리로
                result['emer'] = emer
                result['oper'] = sur
                result['hos'] = str(tfinal[0][2])
                result['time'] = Patient.objects.filter(id = patient_id).values('time')[0]['time']
                result['ETE_S'] = int(Patient.objects.filter(id = patient_id).values('ETE_S')[0]['ETE_S'])
                result['ETE_U'] = int(Patient.objects.filter(id = patient_id).values('ETE_U')[0]['ETE_U'])
                result['ETE_B'] = int(Patient.objects.filter(id = patient_id).values('ETE_B')[0]['ETE_B'])
                result['ETE_C'] = int(Patient.objects.filter(id = patient_id).values('ETE_C')[0]['ETE_C'])
                result['ETA_S'] = t[0]
                result['ETA_U'] = t[1]
                result['ETA_B'] = t[2]
                result['ETA_C'] = t[3]
                result['start'] = timeon(tfinal[0][0],tfinal[0][1])
                result['end'] = timeon(tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])[0],tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])[1])
                result['poss'] = 0
                #db 업데이트 코드
                #선정병원, 예상시작시간, 예상종료시간
                Patient.objects.filter(id = patient_id).update(hos = str(tfinal[0][2]), start = timeon(tfinal[0][0],tfinal[0][1]), end = timeon(tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])[0],tplus(tfinal[0][0],tfinal[0][1],stay[sur][0],stay[sur][1])[1]))
                
                jresult = json.dumps(result)
                
    return render(request, 'emerapp/user_output.html', {'result': jresult})