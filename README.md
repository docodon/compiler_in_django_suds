it is code for online compiler which i made using soappy , django , ideone api .

it is the code for the compiler but simply pulling will not work . you have to add your username and key.

for get it working simply pull it and in compiler_in_django/compile/view.py : add your ideone account name and ideone key at line 13 and 14.

links which helped : http://ideone.com/files/ideone-api.pdf https://ideone.com/files/python-test/ideone.py

and some knowledge of django and html , css and a bit of effort .

some basic info which can be useful :

earlier i had implemented the compiler using soappy and it did work but when i hosted it on pythonanywhere.com then it was not working because it 
of the proxy settings and in soappy i was not able to solve the issues but suds seemed feasible and i changed the code to 
using suds and suds was easy to implement as soappy but then again the issue was there then a bit of googling fetched me the results.


API INFO FOR IDEONE ------------------------------------------------------------------------------

The algorithm of creating a submission and executing it on ideone.com is very simple: ---> Retrieve a list of available programming languages using the getLanguages method.

    getLanguages('user','pass')

    returns : error /language list
---> Create a submission using the createSubmission method.

    createSubmission(user,pass,source_code,language_identifier_int,stdin,\
     run(to run/not program bool value), private (boolean private/public)  )


    returns : identifier of executed program or error if any .
---> Use getSubmissionStatus to check whether ideone.com has finished executing the program. If the program has finished, proceed to step no. 4. Otherwise wait 3­-5 seconds
and repeat step no. 3.

    getSubmissionStatus('user','pass',lang_identifier) 

    returns : error/status/result 

    codes :
    < 0 waiting for compilation – the submission awaits 
    execution in the queue 
    0 done – the program has finished
    1 compilation – the program is being compiled
    3 running – the program is being executed

    0   --> not running – the submission has been created with run parameter set to false
    11  --> compilation error   
    12  --> runtime error  
    13  --> TLEime limit exceeded 
    15  --> success 
    17  --> memory limit exceeded 
    19  --> illegal system call – the program tried to call illegal sytem functions
    20  --> internal error – some problem occurred on ideone.com; 
---> Use getSubmissionDetails to retrieve detailed information about submission :

   getSubmissionDetails(user,pass,lang_identifier,with_source(bool) , with_input()\
            with_output,with_stderr,with_compilation_error)

    returns: 
    error_code , lang_id , lang_name , lang_version , time_of_exec , date(YYYY­MM­DD HH­MM­SS)
    status , memory , signal , public(whetehr code is public or not bool value)
    , source , input , output , stderr , cmpinfo.
----> a function for testing : testFunction('user','pass')
error -> OK/AUTH_ERROR and some more info which is fixed.

here almost each function takes at least 2 parameters --> user and pass(it is the ideone's api key

ideone uses SOAP protocol and its api is available in WSDL format :

SOAP (Simple Object Access Protocol) is a messaging protocol that allows programs that run on disparate operating systems (such as Windows and Linux) to communicate using Hypertext Transfer Protocol (HTTP) and its Extensible Markup Language (XML).

WSDL --> web service description languages .

using SOAPpy in using the WSDL api .
