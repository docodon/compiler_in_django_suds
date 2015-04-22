# -*- coding: utf-8 -*-

from django.shortcuts import render
import suds
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
from time import sleep


#Create_your_views_here.

def home(request) :
	url='https://ideone.com/api/1/service.wsdl'
	user='docodon'
	key='ju#4567'
	context_dict=dict() 
	imp = Import('http://schemas.xmlsoap.org/soap/encoding/')  #simply cut-paste but i think it solves the namespace sort of issues   
	imp.filter.add('http://ideone.com/api/1/service')          #https://fedorahosted.org/suds/ticket/220  (last comment)
	d = ImportDoctor(imp)                                      #without this was not able to fetch from api
	
	if request.method!='POST':		#it is not a post...
		sud_client = Client(url,doctor=d)
		lang_list =sud_client.service.getLanguages(user,key)      #method called using suds_client.service.method  
		
		lang_list =list(lang_list)      #after playing with the hell of this stuff sent by api....i could only manage to get out the
		lang_list=list(lang_list[0][1][1][1])    #and store it in a list of dictionaries named lang
		languages=list()

		for i in lang_list[0][0] :
			temp=dict()
			temp['key']=i[0][0]
			temp['value']=i[1][0]
			languages.append(temp)
		
		context_dict['lang']=languages
		
		return render(request,'compile/home.html',context_dict)
	
	else :                                                                         #when it is a post request....just process code and stdin
		source_code=request.POST.get('source_code')
		stdin=request.POST.get('stdin')
		l_id=request.POST.get('lang')
	

		sud_client = Client(url,doctor=d)
        
		sub=sud_client.service.createSubmission(user,key,source_code,l_id,stdin,True, False)
		link=sub['item'][1]['value'][0]                   #somehow pinned out the link...
        
		
		stts=sud_client.service.getSubmissionStatus(user,key,link)    #checking status if status==0 program executed 
        
		while stts['item'][1]['value'][0]!=0:          
			sleep(2)	
			stts=sud_client.service.getSubmissionStatus(user,key,link)
			
		result=sud_client.service.getSubmissionDetails(user,key,link,True,True,True,True,True)
		context_dict=dict() ;

		for i in result[0] :                               # mostly i made hit & trial for picking up values ...
			context_dict[i[0][0]]=i[1][0]
	
     
		return render(request,'compile/output2.html',context_dict)

