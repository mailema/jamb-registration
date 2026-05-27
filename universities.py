from flask import Flask,session,render_template,redirect,flash,request,send_file
import requests
from bs4 import BeautifulSoup
import re
import random
import os
import datetime

mylist=[]
courselist=[]

url='https://www.unirank.org/ng/a-z/'
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')
universities=soup.find_all('td')
for university in universities:
    univname=university.text
    word=r"University"
    match=re.search(word,univname)
    if match:
        uname=match.string
        mylist.append(uname)
        
      
url="https://exammotives.home.blog/2020/05/08/a-z-of-all-course-offered-in-nigeria/"
#url='https://ulearngo.com/blog/ng/list-of-all-courses-offered-by-nigerian-universities'
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')
#print(soup.prettify())
courses=soup.find_all('strong')
for course in courses:
    coursename=course.text
    courselist.append(coursename)
    #print(course.text)

mobilelist=[]
codelist=['1111111111','0481681813','1754348049','3648484490','4978646016','9784516204','7001248648','1649464648','4000998781','1478646956','9096648484']
#x=random.choice(codelist)
#print(x)
app=Flask(__name__)
app.secret_key='secret'


@app.route("/",methods=['GET','POST'])
def jamblogin():
    if request.method=='POST':
        session['fullname']=request.form['fullname']
        session['email']=request.form['email']
        session['mobile']=request.form['mobile']
        phonenum=session.get('mobile')
        profilecode=request.form['code']
        
        folder="/storage/emulated/0/Download"
        file_name=f"slip_{phonenum}.txt"
        myfile_checker=os.path.join(folder,file_name)
        
        if len(profilecode) != 10:
            flash("Invalid profile code!","fail")
            return render_template('jamblogin.html',codelist=codelist)
        elif profilecode not in codelist:
            flash("Get profile code first!","fail")
            return render_template('jamblogin.html',codelist=codelist)
        elif os.path.exists(myfile_checker):
            flash("phone number already registered","fail")
            return render_template('jamblogin.html',codelist=codelist)            
        else:
            flash("Successful","succeed")
            return redirect('/jambcourses')
    return render_template('jamblogin.html',codelist=codelist)


@app.route('/jambcourses',methods=['GET','POST'])
def jambcourse():
    myname=session.get('fullname')
    if request.method=='POST':
        session['inst1']=request.form['institution1']
        session['crs1']=request.form['course1']
        session['inst2']=request.form['institution2']
        session['crs2']=request.form['course2']
        session['inst3']=request.form['institution3']
        session['crs3']=request.form['course3']
        if session['inst1']==" " or session['crs1']==" " or session['inst2']==" " or session['crs2']==" " or session['inst3']==" " or session['crs3']==" ":
            flash("invalid selection detected","fail")
            return render_template('jambreg.html',myname=myname,mylist=mylist,courselist=courselist)
        else:
            return redirect('/slip')
    return render_template('jambreg.html',myname=myname,mylist=mylist,courselist=courselist)
    
@app.route('/jambcodeengine',methods=['GET','POST'])
def profilecodeengine():
    if request.method=='POST':
        mymobile=request.form['mynumber']
        if len(mymobile) != 11:
            flash("invalid phone number","fail")
            return render_template('jambprofilecode.html')
        else:
            flash("profile code generated successful","succeed")
            return redirect('/jambcode')
    return render_template('jambprofilecode.html')
       
@app.route('/jambcode')
def code():
    session['codelist']=[]
    #session['mycode']=random.randint(1111111111,9999999999)
    #pcode=session.get('mycode')
    pcode=random.choice(codelist)
    return render_template('jambcode.html',pcode=pcode,codelist=codelist)
    
@app.route('/slip', methods=['GET','POST'])  
def slip():
    x=datetime.datetime.today()
    year=x.strftime('%Y')
    alphabets=['A','B','D','E','F','G','H','I','J','K','L','M','N']
    num=random.randint(11111111,99999999)
    letters=random.sample(alphabets,k=2)
    first=letters[0]
    second=letters[1]
    combine=first + second
    session['regnum']=year + str(num) + combine
    regnum=session.get('regnum')
    firstinst=session.get('inst1')
    firstcourse=session.get('crs1')
    secondinst=session.get('inst2')
    secondcourse=session.get('crs2')
    thirdinst=session.get('inst3')
    thirdcourse=session.get('crs3')
    fname=session.get('fullname')
    email=session.get('email')
    mynumber=session.get('mobile')
    return render_template('slip.html',firstinst=firstinst,firstcourse=firstcourse,secondinst=secondinst,secondcourse=secondcourse,thirdinst=thirdinst,thirdcourse=thirdcourse,regnum=regnum,fname=fname,email=email,mynumber=mynumber)


@app.route('/download')
def download():
    #regnum='2026' + str(num) + combine
    myregnum=session.get('regnum')
    firstinst=session.get('inst1')
    firstcourse=session.get('crs1')
    secondinst=session.get('inst2')
    secondcourse=session.get('crs2')
    thirdinst=session.get('inst3')
    thirdcourse=session.get('crs3')
    fname=session.get('fullname')
    email=session.get('email')
    mynumber=session.get('mobile')
    
    #folder="/storage/emulated/0/"
    #new_folder=os.path.join(folder,"Jambfolder")
    #if not os.path.exists(new_folder):
        #os.mkdir(new_folder)
    #else:
        #os.remove(new_folder)   
    #file_path=os.path.join(new_folder,"jambslip.txt")
    phonenum=session.get('mobile')
    folder="/storage/emulated/0/Download"
    file_name=f"slip_{phonenum}.txt"
    session['myfile_path']=os.path.join(folder,file_name)
    file_path=session.get('myfile_path')
    with open(file_path,"w") as file:
        file.write("\n\n____________________________\n\n")
        file.write("JAMB SLIP\n")
        file.write(f"Reg number: {myregnum}\n")
        file.write(f"Name: {fname}\n")
        file.write(f"email: {email}\n")
        file.write(f"phone number: {mynumber}\n\n")
        file.write("\n\n____________________________\n\n")
        file.write("FIRST CHOICE\n")
        file.write(f"institution: {firstinst}\n")
        file.write(f"course: {firstcourse}\n\n")
        file.write("\n\n____________________________\n\n")
        file.write("SECOND CHOICE\n")
        file.write(f"institution: {secondinst}\n")
        file.write(f"course: {secondcourse}\n\n")
        file.write("\n\n____________________________\n\n")
        file.write("THIRD CHOICE\n")
        file.write(f"institution: {thirdinst}\n")
        file.write(f"course: {thirdcourse}\n\n")
        file.write("\n\n____________________________\n\n")
    return send_file(file_path,as_attachment=True)



if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
