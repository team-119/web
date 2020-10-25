from emerapp.models import Patient
from emerapp.forms import PatientForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests
import re
from bs4 import BeautifulSoup as bs
import threading
from datetime import datetime

def user_input(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_id = form.save()
            return redirect('/user_output/{}'.format(patient_id))
        else:
            return HttpResponse("failed")
    else:
        form = PatientForm()
    return render(request, 'emerapp/user_input.html', {'form': form})

def hos_input(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("successfully saved")
        else:
            return HttpResponse("failed")
    else:
        form = PatientForm()
    return render(request, 'emerapp/hos_input.html', {'form': form})

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
    t0 = [] #도착 시간 리스트
    
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
    s1_1 = [] # 성모,수술종류_응급도
    s1_2 = [[0,0,0]]
    s1_3 = []
    s2_1 = []
    s2_2 = []
    s2_3 = []
    s3_1 = []
    s3_2 = []
    s3_3 = []
    s4_1 = []
    s4_2 = []
    s4_3 = []
    s5_1 = []
    s5_2 = []
    s5_3 = []
    s6_1 = []
    s6_2 = [[0,0,0]]
    s6_3 = []
    s7_1 = [[3,3,3]]
    s7_2 = [[1,1,2]]
    s7_3 = [[0,0,0]]
    s8_1 = []
    s8_2 = []
    s8_3 = []
    s9_1 = []
    s9_2 = []
    s9_3 = []
    s10_1 = []
    s10_2 = []
    s10_3 = []
    s11_1 = []
    s11_2 = []
    s11_3 = []
    s12_1 = []
    s12_2 = []
    s12_3 = []
    s13_1 = []
    s13_2 = []
    s13_3 = []
    s14_1 = []
    s14_2 = []
    s14_3 = []
    s15_1 = []
    s15_2 = []
    s15_3 = []
    s16_1 = []
    s16_2 = []
    s16_3 = []
    s17_1 = []
    s17_2 = []
    s17_3 = []
    s18_1 = []
    s18_2 = []
    s18_3 = []
    s19_1 = []
    s19_2 = []
    s19_3 = []
    s20_1 = []
    s20_2 = []
    s20_3 = []
    s21_1 = []
    s21_2 = []
    s21_3 = []
    s22_1 = []
    s22_2 = []
    s22_3 = []
    s23_1 = []
    s23_2 = []
    s23_3 = []
    s24_1 = []
    s24_2 = []
    s24_3 = []
    s25_1 = []
    s25_2 = []
    s25_3 = []
    s26_1 = []
    s26_2 = []
    s26_3 = []
    s27_1 = []
    s27_2 = []
    s27_3 = []
    c1_1 = []
    c1_2 = [[6,6,6]]
    c1_3 = []
    c2_1 = []
    c2_2 = []
    c2_3 = []
    c3_1 = []
    c3_2 = []
    c3_3 = []
    c4_1 = []
    c4_2 = []
    c4_3 = []
    c5_1 = []
    c5_2 = []
    c5_3 = []
    c6_1 = []
    c6_2 = [[1,1,1]]
    c6_3 = []
    c7_1 = [[2,7,11]]
    c7_2 = [[1,2,5]]
    c7_3 = [[0,0,0]]
    c8_1 = []
    c8_2 = []
    c8_3 = []
    c9_1 = []
    c9_2 = []
    c9_3 = []
    c10_1 = []
    c10_2 = []
    c10_3 = []
    c11_1 = []
    c11_2 = []
    c11_3 = []
    c12_1 = []
    c12_2 = []
    c12_3 = []
    c13_1 = []
    c13_2 = []
    c13_3 = []
    c14_1 = []
    c14_2 = []
    c14_3 = []
    c15_1 = []
    c15_2 = []
    c15_3 = []
    c16_1 = []
    c16_2 = []
    c16_3 = []
    c17_1 = []
    c17_2 = []
    c17_3 = []
    c18_1 = []
    c18_2 = []
    c18_3 = []
    c19_1 = []
    c19_2 = []
    c19_3 = []
    c20_1 = []
    c20_2 = []
    c20_3 = []
    c21_1 = []
    c21_2 = []
    c21_3 = []
    c22_1 = []
    c22_2 = []
    c22_3 = []
    c23_1 = []
    c23_2 = []
    c23_3 = []
    c24_1 = []
    c24_2 = []
    c24_3 = []
    c25_1 = []
    c25_2 = []
    c25_3 = []
    c26_1 = []
    c26_2 = []
    c26_3 = []
    c27_1 = []
    c27_2 = []
    c27_3 = [0,0]
    sur_hos = [[ s1_1,s1_2,s1_3,c1_1,c1_2,c1_3 ] ,[ s2_1,s2_2,s2_3,c2_1,c2_2,c2_3 ] ,[ s3_1,s3_2,s3_3,c3_1,c3_2,c3_3 ] ,[ s4_1,s4_2,s4_3,c4_1,c4_2,c4_3 ] ,[ s5_1,s5_2,s5_3,c5_1,c5_2,c5_3 ] ,[ s6_1,s6_2,s6_3,c6_1,c6_2,c6_3 ] ,[ s7_1,s7_2,s7_3,c7_1,c7_2,c7_3 ] ,[ s8_1,s8_2,s8_3,c8_1,c8_2,c8_3 ] ,[ s9_1,s9_2,s9_3,c9_1,c9_2,c9_3 ] ,[ s10_1,s10_2,s10_3,c10_1,c10_2,c10_3 ] ,[ s11_1,s11_2,s11_3,c11_1,c11_2,c11_3 ] ,[ s12_1,s12_2,s12_3,c12_1,c12_2,c12_3 ] ,[ s13_1,s13_2,s13_3,c13_1,c13_2,c13_3 ] ,[ s14_1,s14_2,s14_3,c14_1,c14_2,c14_3 ] ,[ s15_1,s15_2,s15_3,c15_1,c15_2,c15_3 ] ,[ s16_1,s16_2,s16_3,c16_1,c16_2,c16_3 ] ,[ s17_1,s17_2,s17_3,c17_1,c17_2,c17_3 ] ,[ s18_1,s18_2,s18_3,c18_1,c18_2,c18_3 ] ,[ s19_1,s19_2,s19_3,c19_1,c19_2,c19_3 ] ,[ s20_1,s20_2,s20_3,c20_1,c20_2,c20_3 ] ,[ s21_1,s21_2,s21_3,c21_1,c21_2,c21_3 ] ,[ s22_1,s22_2,s22_3,c22_1,c22_2,c22_3 ] ,[ s23_1,s23_2,s23_3,c23_1,c23_2,c23_3 ] ,[ s24_1,s24_2,s24_3,c24_1,c24_2,c24_3 ] ,[ s25_1,s25_2,s25_3,c25_1,c25_2,c25_3 ] ,[ s26_1,s26_2,s26_3,c26_1,c26_2,c26_3 ] ,[ s27_1,s27_2,s27_3,c27_1,c27_2,c27_3 ]]
    stay = [3,5,7,9,11,13,15,17,19,21,23,25,27,30,33,36,39,42,45,48,51,54,57,60,62,64,66,68] #병상 체류시간
    
    
    # 여기서부터 반복
    # 1. DB는 1분마다 반복
    # 2. 본체는 정보 들어올때마다

    #DB 연동 코드
    #직접 온 사람 정보 
    
    def fromdb():
        #수술실 타임라인 가져오기
        #지금 있는거보다 더 많으면 가져오기
        #아니면 직접 온 사람일때 가져오기 (by = 1)
        p = Patient.objects.get(id=patient_id)
        n = Patient.objects.count()
        t0 = datetime.today() 
        tfinal = 0 
        sur = p.oper
        emer = p.emer

        for i in range(n,0,-1): #뒤에서 몇번째
            if sur[i] !=0: #수술 필요시
                if sur_hos[sur-1][emer-1][-1][0] < p.id[i]: #환자코드가 더 크면    
                    if p[i].by == 1: #병원에서 온 사람 
                        if p[i].hos == 'S': #성모 병원 간 사람 
                            if sur_hos[sur-1][emer-1][-1][2] <= t0: #도착하자마자 가능 
                                    tfinal = t0
                            else: #기다려야됨
                                tfinal = sur_hos[sur-1][emer-1][-1][2]
                            sur_hos[sur-1][emer-1].append([p[i].id,tfinal,tfinal + stay[sur[i]]]) #p.oper[i]
    
                        elif p[i].hos == 'C': #추병원 간 사람 
                            if sur_hos[sur-1][emer+2][-1][2] <= t0: #도착하자마자 가능 
                                tfinal = t0
                            else: #기다려야됨
                                tfinal = sur_hos[sur-1][emer+2][-1][2]
                            sur_hos[sur-1][emer+2].append([p[i].id,tfinal,tfinal + stay[sur[i]]])
    
                        else :
                            continue 
                            
                else:
                    break
        threading.Timer(60,fromdb).start()
    
    fromdb()
    

    p = Patient.objects
    pn = p.filter(by = 0).order_by('id').last() # 환자 코드 
    t0 = [p[pn].ETA_S, p[pn].ETA_U, p[pn].ETA_B, p[pn].ETA_C] # 병원별 도착 시간
    emer = p.emer[pn]
    sur = p.oper[pn]
    
    
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

    
    # 체크리스트에서 sur 받아오기 
    # t0 받아오는 코드 
    # 가능한 병원 찾기
    
    sur = 7 # 치료종류
    poss_hos = [0,0,0,0] # 가능한 병원(병원순서대로 칸 번호)
    tfinal = [] # 최종 치료 가능 시작 시간 
    emer = 2 #응급도 점점 응급
    poss_hos = [-1,-1,-1,-1]
    emer = 2
    patient = [pn]
    t0 = [4,3,2,1]
    pn = 102111
    
    if sur == 0: #중증X -> 응급실 유무만
        n = 0
        for i in number:
            if int(i[0]) < int(i[1]): #병상 있으면 가능(1)
                poss_hos[n] = 1 
                tfinal.append([t0[n],n]) #가능하면 [t0,병원숫자](가까운데로)
                print(tfinal[n])
            else: #없으면 불가능(0)
                poss_hos[n] = 0
            n+=1
        #이때는 바로 tfinal sort로 넘어가면 됨 
        tfinal = qsort(tfinal)
        print(tfinal)
        for i in tfinal:
            print(name_hos[i[1]],i[0])
            
    else: #(poss_hos에 병원 2개) (성모,추)
        n = 0
        if sungmo_sur[sur] == 1:
            poss_hos[0] = 3 #성모 가능
            #ting.append(t0[0])
        
        elif sungmo_sur[sur] == 0 or 2:
            poss_hos[0] = 2 #성모 불가능 
        
        if chu_sur[sur] == 1:
            poss_hos[3] = 3 #추 가능   
            #ting.append(t0[3])
     
        elif chu_sur[sur] == 0 or 2:
            poss_hos[3] = 2 #추 불가능 
        n+=1
        
        #병원 별로 도착시간과 같은 응급도 타임라인에서 마지막 치료종료시간과 비교  
        if poss_hos[0] == 3: #0,3 => 성모 가능 
            if sur_hos[sur-1][emer-1][-1][2] <= t0[0]: #도착하자마자 가능 
                tfinal.append([t0[0],0])
            else: #기다려야됨
                tfinal.append([sur_hos[sur-1][emer-1][-1][2],0])
    
        if poss_hos[3] == 3: #3,3 => 추 가능
            if sur_hos[sur-1][emer+2][-1][2] <= t0[3]: #종료시간과 도착 시간 비교 
                tfinal.append([t0[3],3])
            else:
                tfinal.append([sur_hos[sur-1][emer+2][-1][2],3])
    
        #tfinal 정렬 
        tfinal = qsort(tfinal)
    
        #환자, 타임라인 업데이트
        patient.extend([tfinal[0][1],tfinal[0][0],tfinal[0][0]+stay[sur]]) # 정한 병원, tfinal, 예상 완료시간
        if sur != 0:
            sur_hos[sur-1][emer-1+tfinal[0][1]].append([pn,tfinal[0][0],tfinal[0][0]+stay[sur]]) #0 emer-1 / 3 emer+2
    
        #응급도별 타임라인 시간 조정 (1일때는 변화 X)
        gaptime = 0
        if emer == 3: #응급도 클수록 우선
            if sur_hos[sur-1][emer-2+tfinal[0][1]][0][1] >= sur_hos[sur-1][emer-1+tfinal[0][1]][-1][2]: #도착 시간이 더 늦어서 변동X
                gaptime = 0
            else :
                gaptime = sur_hos[sur-1][emer-1+tfinal[0][1]][-1][2] - sur_hos[sur-1][emer-2+tfinal[0][1]][0][1]
                for i in sur_hos[sur-1][emer-2+tfinal[0][1]]:
                    i[1] += gaptime
                    i[2] += gaptime
    
            if sur_hos[sur-1][emer-3+tfinal[0][1]][0][1] >= sur_hos[sur-1][emer-2+tfinal[0][1]][-1][2]: #도착 시간이 더 늦어서 변동X
                gaptime = 0
            else:
                gaptime = sur_hos[sur-1][emer-2+tfinal[0][1]][-1][2] - sur_hos[sur-1][emer-3+tfinal[0][1]][0][1]
                for i in sur_hos[sur-1][emer-3+tfinal[0][1]]:
                    i[1] += gaptime
                    i[2] += gaptime
    
        elif emer == 2:
            if sur_hos[sur-1][emer-2+tfinal[0][1]][0][1] >= sur_hos[sur-1][emer-1+tfinal[0][1]][-1][2]: #도착 시간이 더 늦어서 변동X
                gaptime = 0
            else :
                gaptime = sur_hos[sur-1][emer-1+tfinal[0][1]][-1][2] - sur_hos[sur-1][emer-2+tfinal[0][1]][0][1]
                for i in sur_hos[sur-1][emer-2+tfinal[0][1]]:
                    i[1] += gaptime
                    i[2] += gaptime
    
        result = [] #출력할 결과물
        #출력
        for i in tfinal:
            result.append([name_hos[i[1]],t0[i[1]],i[0]])
        print(result)
        print(tfinal)

    
    #db 업데이트 코드 
    #선정병원, 예상시작시간, 예상종료시간
    hosname = ['S','U','B','C']
    p1 = Patient.objects.get(id = pn)
    p1.hos = hosname[tfinal[0][1]]
    p1.start = tfinal[0][1]
    p1.end = tfinal[0][2]
    p1.save()
                
    return render(request, 'emerapp/user_output.html', {'result': result})