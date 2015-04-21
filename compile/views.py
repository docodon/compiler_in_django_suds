# -*- coding: utf-8 -*-

from django.shortcuts import render
import SOAPpy
from SOAPpy import WSDL
from time import sleep


#Create_your_views_here.

def home(request) :
	url='https://ideone.com/api/1/service.wsdl'
	user=''
	key=''
	context_dict=dict() 
	if request.method!='POST':		#it is not a post...
		
		wsdlObject = WSDL.Proxy(url)
		lang_list =SOAPpy.Types.simplify(wsdlObject.getLanguages(user,key))   
		languages=lang_list['item'][1]['value']['item']
		context_dict['lang']=languages
		#print context_dict['lang']
		return render(request,'compile/home.html',context_dict)
	
	else :
		source_code=request.POST.get('source_code')
		stdin=request.POST.get('stdin')
		l_id=request.POST.get('lang')
		#print source_code
		#print l_id

		wsdlObject = WSDL.Proxy(url)
        
		sub=SOAPpy.Types.simplify(wsdlObject.createSubmission(user,key,source_code,l_id,stdin,True, False))
		link=sub['item'][1]['value']

		stts=SOAPpy.Types.simplify(wsdlObject.getSubmissionStatus(user,key,link))

		while stts['item'][1]['value']!=0:
			sleep(2)	
			stts=SOAPpy.Types.simplify(wsdlObject.getSubmissionStatus(user,key,link))
		
		result=SOAPpy.Types.simplify(wsdlObject.getSubmissionDetails(user,key,link,True,True,True,True,True))
		context_dict=dict() ;

		for i in result['item'] :
			context_dict[i['key']]=i['value']
		
		context_dict['12']='runtime error'
		context_dict['13']='time limit exceeded'
		context_dict['19']='illegal system call'
		context_dict['20']='internal error on  ideone.com . try to re-submit and if fails, then please contact at contact@ideone.com '
		context_dict['17']='memory limit exceeded'

		return render(request,'compile/output2.html',context_dict)

