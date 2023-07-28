from django.shortcuts import render,redirect
from django.contrib import messages
from Home.models import User,problems, testcases
from django.contrib.auth.hashers import *
import math
import random
from Home.apicall import data
from Home.otpAuthentication import send_otp
# Create your views here.

def admin(request):
    try:
        context={}
        if("type" in request.session.keys() and request.session["type"] != "Admin"):
            if(request.session["type"] == "Participant"):
                return redirect("/")
            
        elif("otp" in request.session.keys() and not request.session["otp"]):
            return redirect("/login/")
        
        elif("type" in request.session.keys() and request.session["otp"]):
            questions=problems.objects.filter(adminEmail = request.session["user"]).all()
            context["questions"]=questions
            print("Hello world")

        return render(request, "admin.html", context)
    except:
        return redirect("/login/")
def index(request):
    try:
        context={}
        if("type" in request.session.keys() and request.session["type"] != "Participant"):
            if(not request.session["otp"]):
                return redirect("/login/")
            elif(request.session["type"] == "Admin" and request.session["otp"]):
                return redirect("/admin/")
            return redirect("/login/")
        
        elif("otp" in request.session.keys() and not request.session["otp"]):
            return redirect("/login/")
        
        elif("type" in request.session.keys() and request.session["otp"]):
            backgroundcolor=""
            messageTitle = ""
            m_output=""
            code=""
            language=""
            if request.method == "POST":
                language=request.POST.get("language")
                code=request.POST.get("code")
                input=request.POST.get("input")
                code=code
                input
                if(language == "C"):
                    language = "c"
                elif(language == "C#"):
                    language = "csharp"
                elif(language == "C++"):
                    language = "cpp17"
                elif(language == "Go"):
                    language = "go"
                elif(language == "Java"):
                    language = "java"
                elif(language == "JavaScript"):
                    language = "nodejs"
                elif(language == "Kotlin"):
                    language = "kotlin"
                elif(language == "Python"):
                    language = "python3"
                dict=data(code, language, input)

                m_output=dict['output']
                if("error" in dict['output'].lower()):
                    backgroundcolor = "#c20e0e"
                    messageTitle="Error"
                    messages.success(request, ' ')
                else:
                    backgroundcolor = "#4BB543"
                    messageTitle="Sucessful"
                    messages.success(request, ' ')

            user_data = problems.objects.all()
            totalPages = math.ceil(user_data.count() / 1)
            pageNumber = request.GET.get("page")
            if(pageNumber == None):
                pageNumber = 1
            else:
                pageNumber=int(pageNumber)
            posts = user_data[(pageNumber - 1) * 1 : (pageNumber - 1) * 1 + 1]
            if(totalPages == 1):
                previous="#"
                next="#"
            elif(pageNumber == 1):
                previous="#"
                next="/?page="+ str(pageNumber + 1)
            elif(pageNumber == totalPages):
                previous="/?page="+ str(pageNumber - 1)
                next="#"
            else:
                previous="/?page="+ str(pageNumber - 1)
                next="/?page="+ str(pageNumber + 1)
            
            if(len(posts) > 0):
                test=testcases.objects.filter(questionId = posts[0].sno).all()
            else:
                test=""
            context={
                "b_color": backgroundcolor,
                "m_title":messageTitle,
                "m_output": m_output,  
                "questions": posts,
                "testcases": test,
                "next": next,
                "previous": previous,
                "code": code,
                "language": language
            }
        context=context
        return render(request, "index.html", context)
    except:
        return redirect("/login/")
def login_page(request):
    try:
        if(request.method == "POST"):
            global generateOTP
            name=request.POST.get("name")
            email=request.POST.get("email")
            role=request.POST.get("role")
            password=request.POST.get("password")

            if(role == "Participant"):
                user_data=User.objects.filter(email = email, role = role).first()
                if(user_data == None):
                    messages.info(request, "Participant not exists")
                    return redirect("/login/")
                elif(not check_password(password, user_data.password)):
                    messages.warning(request, "Password Incorect")
                    return redirect("/login/")
                
                elif(name != user_data.username):
                    messages.warning(request, "Username Incorect")
                    return redirect("/login/")
                else:
                    generateOTP = random.randint(1000, 9999)
                    send_otp(generateOTP, email)
                    request.session["logdin"]=True
                    request.session["user"]=email
                    request.session["type"]=role
                    request.session["otp"]=False
                    return redirect("/otp_verification/")
            elif(role == "Admin"):
                user_data=User.objects.filter(email = email, role = role).first()
                if(user_data == None):
                    messages.info(request, "Admin not exists")
                    return redirect("/login/")
                elif(not check_password(password, user_data.password)):
                    messages.warning(request, "Password Incorect")
                    return redirect("/login/")
                elif(name != user_data.username):
                    messages.warning(request, "Admin name Incorect")
                    return redirect("/login/")
                else:
                    generateOTP = random.randint(1000, 9999)
                    send_otp(generateOTP, email)
                    request.session["logdin"]=True
                    request.session["user"]=email
                    request.session["type"]=role
                    request.session["otp"]=False
                    return redirect("/otp_verification/")
        return render(request, "login.html")
    except:
        return redirect("/login/")

def signup_page(request):
    try:
        if(request.method == "POST"):
            name=request.POST.get("name")
            email=request.POST.get("email")
            role=request.POST.get("role")
            password=request.POST.get("password")
            repassword=request.POST.get("repassword")

            if(role == "Participant"):
                user_data=User.objects.filter(email = email, role = role).first()
                if(user_data != None):
                    messages.warning(request, "Participant alrady Exists ")
                    return redirect("/signup/")
                elif(password != repassword):
                    messages.warning(request, "Password and Repassword is not same ")
                    return redirect("/signup/")
                else:
                    entery=User(username = name, email = email, role=role, password = make_password(password))
                    entery.save()
                    return redirect("/login/")
            elif(role == "Admin"):
                user_data=User.objects.filter(email = email, role = role).first()
                if(user_data != None):
                    messages.warning(request, "Admin alrady Exists ")
                    return redirect("/signup/")
                elif(password != repassword):
                    messages.warning(request, "Password and Repassword is not same ")
                    return redirect("/signup/")
                else:
                    entery=User(username = name, email = email, role=role, password = make_password(password))
                    entery.save()
                    return redirect("/login/")
        return render(request, "signup.html")
    except:
        return redirect("/login/")
def otp_verification(request):
    try:
        if request.method == 'POST':
            otp=request.POST.get("otp")
            print(f"This is the opt {generateOTP}")
            if(generateOTP == int(otp)):
                request.session["otp"]=True
                return redirect("/")
            else:
                messages.error(request,"OTP not correct")
        return render(request, "otp.html")
    except:
        return redirect("/login/")
def addQuestion(request):
    try:
        if("logdin" in request.session.keys() and request.session["type"] == "Admin"):
            if request.method == "POST":
                title=request.POST.get("title")
                question=request.POST.get("question")
                testcaseInput=request.POST.get("input")
                testcaseOutput=request.POST.get("output")
                addProblem = problems(adminEmail = request.session["user"], title = title, question = question)
                addProblem.save()
                addTestcase = testcases(adminEmail = request.session["user"], questionId = addProblem.sno, input = testcaseInput, output = testcaseOutput)
                addTestcase.save()
                return redirect("/admin/")
        elif("logdin" not in request.session.keys() or request.session["type"] != "Admin"):
            return redirect("/login/")
        return render(request, "addquestion.html")
    except:
        return redirect("/login/")
def logout(request):
    request.session.clear()
    return redirect("/")
def views(request, questionId):
    try:
        if("logdin" in request.session.keys() and request.session["type"] == "Admin"):
            ques=problems.objects.filter(adminEmail = request.session["user"], sno = questionId).first()
            test=testcases.objects.filter(adminEmail = request.session["user"], questionId = questionId).all()
            context={
                "question": ques,
                "testcase": test
            }
            return render(request, "views.html", context)
        else:
            return redirect("/login/")
    except:
        return redirect("/login/")
def edit(request, number):
    try:
        if request.method == "POST":
            title=request.POST.get("title")
            question=request.POST.get("question")

            addProblem=problems.objects.filter(adminEmail = request.session["user"], sno=number).first()

            addProblem.title=title
            addProblem.question=question
            addProblem.save()
            return redirect(f"/edit/{number}")
        else:
            data=problems.objects.filter(adminEmail = request.session["user"], sno=number).first()
            tast=testcases.objects.filter(adminEmail = request.session["user"], questionId = data.sno).all()
            context={
                "data": data,
                "testcases": tast
            }
            return render(request, "edit.html", context)
    except:
        return redirect("/login/")
def delete(request, number):
    try:
        problem=problems.objects.filter(sno=number).first()
        testcas=testcases.objects.filter(questionId = number).all()

        problem.delete()
        testcas.delete()

        return redirect("/admin/")
    except:
        return redirect("/login/")
def questions(request):
    return render(request, "addquestion.html")

def editTestcase(request, questionId, testcasenumber):
    try:
        if("logdin" in request.session.keys() and request.session["type"] == "Admin"):
            if request.method == "POST":
                input=request.POST.get("input")
                output=request.POST.get("output")
                test=testcases.objects.filter(questionId = questionId, sno= testcasenumber).first()
                test.input=input
                test.output=output
                test.save()
                return redirect(f"/edit/{questionId}")
        else:
            return redirect("/login/")
    except:
        return redirect("/login/")
    
def deleteTestcase(request, questionId, testcasenumber):
    try:
        if("logdin" in request.session.keys() and request.session["type"] == "Admin"):
            test=testcases.objects.filter(questionId = questionId, sno= testcasenumber).first()
            test.delete()
            return redirect(f"/edit/{questionId}")
        else:
            return redirect("/login/")
    except:
        return redirect("/login/")
def addTestcase(request, questionId):
    try:
        if("logdin" in request.session.keys() and request.session["type"] == "Admin"):
            if request.method == "POST":
                input=request.POST.get("input")
                output=request.POST.get("output")
                test=testcases(questionId = questionId, input = input, output = output, adminEmail = request.session["user"])
                test.save()
            return redirect(f"/edit/{questionId}")
        else:
            return redirect("/login/")
    except:
        return redirect("/login/")