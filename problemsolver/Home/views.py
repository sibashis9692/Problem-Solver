from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from Home.models import User,problems, testcases
from django.contrib.auth.hashers import *
import math
# Create your views here.

def admin(request):
    if("type" in request.session.keys() and request.session["type"] != "Admin"):
        if("type" in request.session.keys() and request.session["type"] == "Participant"):
            return redirect("/")
        return redirect("/login/")
    else:
        context={}
        questions=problems.objects.filter(adminEmail = request.session["user"]).all()
        context["questions"]=questions
    return render(request, "admin.html", context)
def index(request):
    if("type" in request.session.keys() and request.session["type"] != "Participant"):
        if("type" in request.session.keys() and request.session["type"] == "Admin"):
            return redirect("/admin/")
        return redirect("/login/")
    else:
        user_data= problems.objects.all()
        totalPages= math.ceil(len(user_data) / 1)
        pageNumber=request.GET.get("page")
        if(pageNumber == None):
            pageNumber = 1
        else:
            pageNumber=int(pageNumber)
        posts = user_data[(pageNumber - 1) * 1 : (pageNumber - 1) * 1 + 1]
        print(f"totalPage: {totalPages}")
        print(f"currentPage: {pageNumber}")
        if(totalPages == 1):
            previous="#"
            next="#"
        elif(pageNumber == 1):
            print("i am 1")
            previous="#"
            next="/?page="+ str(pageNumber + 1)
        elif(pageNumber == totalPages):
            print("i am 2")
            previous="/?page="+ str(pageNumber - 1)
            next="#"
        else:
            print("i am 3")
            previous="/?page="+ str(pageNumber - 1)
            next="/?page="+ str(pageNumber + 1)
        context={
            "questions": posts,
            "next": next,
            "previous": previous
        }
    return render(request, "index.html", context)

def login_page(request):
    if(request.method == "POST"):
        name=request.POST.get("name")
        email=request.POST.get("email")
        role=request.POST.get("role")
        password=request.POST.get("password")

        if(role == "Participant"):
            user_data=User.objects.filter(email = email, role = role).first()
            if(user_data == None):
                messages.info(request, "Participant not exists")
                return redirect("/login/")
            if(not check_password(password, user_data.password)):
                messages.warning(request, "Password Incorect")
                return redirect("/login/")
            else:
                request.session["logdin"]=True
                request.session["user"]=email
                request.session["type"]=role
                return redirect("/")
        elif(role == "Admin"):
            user_data=User.objects.filter(email = email, role = role).first()
            if(user_data == None):
                messages.info(request, "Admin not exists")
                return redirect("/login/")
            if(not check_password(password, user_data.password)):
                messages.warning(request, "Password Incorect")
                return redirect("/login/")
            else:
                request.session["logdin"]=True
                request.session["user"]=email
                request.session["type"]=role
                return redirect("/admin/")
    return render(request, "login.html")

def signup_page(request):
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

def addQuestion(request):
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
def logout(request):
    request.session.clear()
    return redirect("/")
def views(request, number):
    if("logdin" in request.session.keys() and request.session["type"] == "Admin"):
        data=problems.objects.filter(sno = number).first()
        data1=testcases.objects.filter(questionId = number).all()
        context={
            "question": data,
            "testcase": data1
        }
        return render(request, "views.html", context)
    else:
        return redirect("/login/")
def edit(request, number):
    if request.method == "POST":
        title=request.POST.get("title")
        question=request.POST.get("question")
        testcaseInput=request.POST.get("input")
        testcaseOutput=request.POST.get("output")

        addProblem = problems.objects.filter(sno = number).first()
        addProblem = testcases.objects.filter(sno = number).first()
        addProblem.title=title
        addProblem.question=question
        addProblem.save()

        addTestcase = testcases(adminEmail = request.session["user"], questionId = addProblem.sno, input = testcaseInput, output = testcaseOutput)
        addTestcase.save()
    else:

        data=problems.objects.filter(adminEmail = request.session["user"], sno=number).first()
        context={
            "data": data,
        }
        return render(request, "edit.html", context)

def delete(request, number):
    problem=problems.objects.filter(sno=number).first()
    testcas=testcases.objects.filter(questionId = number).all()

    problem.delete()
    testcas.delete()

    return redirect("/admin/")
def questions(request):
    return render(request, "addquestion.html")