from django.shortcuts import HttpResponse,render,redirect
from Admin.models import Userinfo,userpost,followers 
from User.functions import handle_uploaded_file 
from datetime import datetime 
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def hellouser(request):
    return HttpResponse ('Hello user')

def login(request):
    return render(request,"login.html",{})

def register(request):
    return render(request,"signup.html",{})

def info(request):
    if(request.method == "GET"):
        return render(request,"signup.html",{})
    else:
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        bday = request.POST["bday"]
        location = request.POST["location"]
        print(fname,lname,email,password,phone,bday,location)
        user = Userinfo()
        user.fname = fname
        user.lname = lname
        user.email = email
        user.password = password
        user.phone = phone
        user.bday = bday
        user.location = location
        user.save()
        print("save")
        request.session["email"]=email
        return render(request,"info.html",{"fname":fname})

def successfull(request):
    if("email" in request.session):
        email = request.session["email"]
        print(email)
        print("succesful")
        profile =request.FILES['profil']
        cover =request.FILES['cover']
        '''handle_uploaded_file(request.FILES['profil'])
        print("--------------",handle_uploaded_file(request.FILES['profil']))
        handle_uploaded_file(request.FILES['cover'])
        print("--------------",handle_uploaded_file(request.FILES['cover']))'''
        handle_uploaded_file((profile))
        handle_uploaded_file((cover))

        #profile =request.FILES['profil']
        print("profile url- ",profile)
        print("cover url",cover)
        #cover =request.FILES['cover']
        Bio =request.POST["Bio"]
        user = request.session["email"]
        user = Userinfo.objects.get(email=user)
        print("object fetched")
        user.profil=profile
        user.cover=cover
        user.Bio=Bio
        user.save()
        print(email)
        print("--",settings.EMAIL_HOST_USER)
        msg = """
        Hello,

        Welcome to WeShare. We are Happy to see you here!

        We are confident that WeShare will help you to 
        connect people and much more.

        You can also Post it Here with your beautiful Images.

        Have a Good Day ahead..!

        
        
        Thank You,
        WeShare Community.
        """
        #below code is used for sending mail
        send_mail("Welcome to WeShare",msg,'settings.EMAIL_HOST_USER',[email],fail_silently=False)
        #after signup direct user can see login page
        suggetion = []
        try:
            user = Userinfo.objects.get(email=email)
        except:
            return render(request,"login.html",{}) 
        else:
            
            data = str((user.joining))
            data = data[0:11]
            print("joining date : ",data)
            users = Userinfo.objects.all()
            for i in users:

                if(str(i.email) == email):
                    continue
                else:
                    suggetion.append(i)

            users = suggetion
            return render(request,"home.html",{"user":user,"joiningtime":data,"all":users})
    else:
        return render(request,"login.html",{})  
            
def home(request):
    if(request.method == "GET"):
        if "email" in request.session:
            email=request.session["email"]
            useremail = request.session["email"]
            
            try:
                user = Userinfo.objects.get(email=email)
            except:
                return render(request,"login.html",{}) 
            else:
              
                joiningtime = str((user.joining))
                joiningtime = joiningtime[0:11]
                print("joining date : ",joiningtime)

                post = userpost.objects.filter(user_id=user)
                
                user = Userinfo.objects.get(email = useremail)
    
                datass = followers.objects.filter(user_id=user)
                new = []
                new1 = []
                for i in datass:
                    new.append(i.frinds)
                print(new)
                for x in new:
                    myfriends = Userinfo.objects.get(id = x)
                    print(str(myfriends))
                    new1.append(myfriends)
                print(new1)
                size = len(new1)

                suggetion_for_you = []
                
                alluser = Userinfo.objects.all()
                print("All user:-",alluser)
                for i in alluser:
                    print(i.email)
                    print(i)
                    if(str(i.email) == useremail) or (i in new1):
                        print("********")
                        continue
                    else:
                        suggetion_for_you.append(i)
                return render(request,"home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":suggetion_for_you,"size":size})
            
        else:

            return render(request,"login.html",{})
    else:
        email =request.POST["email"]
        password =request.POST["password"]
        request.session["email"]=email
        suggetion = []
        try:
            user = Userinfo.objects.get(email=email,password=password)
        except:
            return render(request,"login.html",{}) 
        else:
            x = ''
            joiningtime = str((user.joining))
            joiningtime = joiningtime[0:11]
            print("joining date : ",joiningtime)

            post = userpost.objects.filter(user_id=user)
            
            users = Userinfo.objects.all()
            for i in users:
                if(str(i.email) == email):
                    continue
                else:
                    suggetion.append(i)
            users = suggetion
            return render(request,"home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":users})
            
def logout(request):
    request.session.clear()
    return redirect(login)

def addpost(request):
    print("***************************************************")
    if "email" in request.session:
        useremail = request.session["email"]
        
        user = Userinfo.objects.get(email=useremail)
        
        caption = request.POST["caption"]
        print(caption)
        handle_uploaded_file(request.FILES['postphoto'])
        postphoto =request.FILES['postphoto']
        print(postphoto)
        post = userpost()
        post.caption = caption
        post.postphoto = postphoto
        post.user = user
        post.save()
        joiningtime= str(post.posttime)
        joiningtime = joiningtime[0:16]
        print("save")
        users = Userinfo.objects.all()
        datas = userpost.objects.filter(user_id=user)
        print(datas,"****************************")

        user = Userinfo.objects.get(email = useremail)
    
        datass = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datass:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
        
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        return render(request,"home.html",{"user":user,"datas":datas,"joiningtime":joiningtime,"all":suggetion_for_you})

def about(request):
    useremail = request.session["email"]
    print(useremail)
    user = Userinfo.objects.get(email = useremail)
    print(user)
    post = userpost.objects.filter(user_id=user)
    
    joiningtime = str((user.joining))
    joiningtime = joiningtime[0:11]
    '''suggetion = []
    alluser = Userinfo.objects.all()
    for i in alluser:

        if(str(i.email) == useremail):
            continue
        else:
            suggetion.append(i)'''


    user = Userinfo.objects.get(email = useremail)
    
    datass = followers.objects.filter(user_id=user)
    new = []
    new1 = []
    for i in datass:
        new.append(i.frinds)
    print(new)
    for x in new:
        myfriends = Userinfo.objects.get(id = x)
        print(str(myfriends))
        new1.append(myfriends)
    print(new1)
    size = len(new1)

    suggetion_for_you = []
    
    alluser = Userinfo.objects.all()
    print("All user:-",alluser)
    for i in alluser:
        print(i.email)
        print(i)
        if(str(i.email) == useremail) or (i in new1):
            print("********")
            continue
        else:
            suggetion_for_you.append(i)
    print(alluser)
    print(suggetion_for_you)
    return render(request,"about.html",{"user":user,"all":suggetion_for_you,"datas":post,"joiningtime":joiningtime,"size":size})

def timeline(request):
    if "email" in request.session:
        useremail = request.session["email"]
        print(useremail)
        user = Userinfo.objects.get(email=useremail)
        print(user)
        post = userpost.objects.filter(user_id=user)
        print(post)
        
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        '''suggetion = []
        alluser = Userinfo.objects.all()
        for i in alluser:

            if(str(i.email) == useremail):
                continue
            else:
                suggetion.append(i)'''
        user = Userinfo.objects.get(email = useremail)
        
        datass = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datass:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        
        
        

        
        return render(request,"home.html",{"user":user,"datas":post,"all":suggetion_for_you,"joiningtime":joiningtime,"size":size})

def photos(request):
    if "email" in request.session:
        
        useremail = request.session["email"]
        user = Userinfo.objects.get(email = useremail)
        post = userpost.objects.filter(user_id=user)
        alluser = Userinfo.objects.all()
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]

        '''suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        for i in alluser:

            if(str(i.email) == useremail):
                continue
            else:
                suggetion_for_you.append(i)
        print(suggetion_for_you)'''
        user = Userinfo.objects.get(email = useremail)
        
        datass = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datass:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)


        return render(request,"photos.html",{"datas":post,"user":user,"all":suggetion_for_you,"joiningtime":joiningtime,"size":size})

def friends(request,id):
    if "email" in request.session:
        
        useremail = request.session["email"]
        user = Userinfo.objects.get(email = useremail)
        post = userpost.objects.filter(user_id=id)
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        user = Userinfo.objects.get(email = useremail)
        
        datas = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datas:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        following = followers.objects.filter(user_id=user)

        #for my frinds section
        friend = []
        final_friend=[]
        for i in following:
            friend.append(i)
            print("My following",i.frinds)
        for y in friend:

            frinds = Userinfo.objects.get(id = y.frinds)
            final_friend.append(frinds)
        print("my final frinds id: -",final_friend)

        return render(request,"following.html",{"user":user,"all":suggetion_for_you,"datas":post,"size":size,"joiningtime":joiningtime,"following":final_friend})
    
def forgot(request):
    return render(request,"forgot.html",{})

def updatepassword(request):
    if request.method == 'GET':
        return render(request,"forgot.html",{})
    else:
        
        email = request.POST["email"]
        phone = request.POST["phone"]
        try:

            user= Userinfo.objects.get(email=email,phone=phone)
            
        except:
            return render(request,"forgot.html",{})
        else:
            request.session["email"]=email
            return render(request,"changepassword.html",{"user":user})

def save(request):
    if "email" in request.session:
        useremail = request.session["email"]
        enter = request.POST["enter"]
        re_enter = request.POST["re-enter"]
        if (enter == re_enter):
            user = Userinfo.objects.get(email =useremail)
            user.password = enter
            user.save()
            return redirect(login)
        else:
            return render(request,"changepassword.html",{})

def following(request,id):
    #if(request.method == "post"):
    if "email" in request.session:
        print(id)
        
        useremail = request.session["email"]
        user = Userinfo.objects.get(email = useremail)
        post = userpost.objects.filter(user_id=id)
        print(len(post))
        print("posts:- ",post)
        print(user)
        print(id)
        print("*******************************************",id)
        f1 = followers()
        f1.user = user
        f1.frinds = id
        print("-------------------------------------------------------",f1)
        f1.save()
        
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        user = Userinfo.objects.get(email = useremail)
        
        myfriends = followers.objects.filter(user_id=user)
        print("-------------------------------",myfriends,"------------")
        new = []
        new1 = []
        for i in myfriends:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
    
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        following = followers.objects.filter(user_id=id)


        friend = []
        final_friend=[]
        for i in following:
            friend.append(i)
            print("My following",i.frinds)
        for y in friend:

            frinds = Userinfo.objects.get(id = y.frinds)
            final_friend.append(frinds)
        print("my final frinds id: -",final_friend)


        return render(request,"following.html",{"user":user,"friends":new1,"datas":post,"all":suggetion_for_you,"size":size,"joiningtime":joiningtime,"following":final_friend})

    '''else:
        
        if "email" in request.session:
            
            useremail = request.session["email"]
            user = Userinfo.objects.get(email = useremail)
            post = userpost.objects.filter(user_id=user)
            print("posts:- ",post)

           
            
            joiningtime = str((user.joining))
            joiningtime = joiningtime[0:11]
            user = Userinfo.objects.get(email = useremail)
            
            datas = followers.objects.filter(user_id=user)
            new = []
            new1 = []
            for i in datas:
                new.append(i.frinds)
            print(new)
            for x in new:
                myfriends = Userinfo.objects.get(id = x)
                print(str(myfriends))
                new1.append(myfriends)
            print(new1)
            size = len(new1)

            suggetion_for_you = []
        
            alluser = Userinfo.objects.all()
            print("All user:-",alluser)
            for i in alluser:
                print(i.email)
                print(i)
                if(str(i.email) == useremail) or (i in new1):
                    print("********")
                    continue
                else:
                    suggetion_for_you.append(i)
            print(alluser)
            print(suggetion_for_you)
            


            return render(request,"following.html",{"user":user,"all":suggetion_for_you,"data":post,"datas":new1,"size":size,"joiningtime":joiningtime})'''

def editprofile(request,id):
    user= Userinfo.objects.get(id = id)
    bday = str(user.bday)
    bday = bday[:10:]
    return render(request,"editprofile.html",{"user":user,"bday":bday})

def edited(request,id):

    if("email" in request.session):
        email = request.session["email"]
        user = Userinfo.objects.get(id = id)
        
        profil = user.profil
        cover= user.cover
        user.fname =request.POST["fname"]
        user.lname =request.POST["lname"]
        user.email =request.POST["email"]
        user.password =request.POST["password"]
        user.phone =request.POST["phone"]
        user.location =request.POST["location"]
        user.bday =request.POST["bday"]
        
        try:
            try:
                handle_uploaded_file(request.FILES['profil'])
                user.profil = request.FILES['profil']

                
                
            except:
                user.profil =profil
                

            try:

                handle_uploaded_file(request.FILES['cover'])
                
                user.cover =request.FILES['cover']
                    
            except:
                user.cover =cover
                   

        except:
            user.profil =profil
            user.cover =cover
            
            user.save()

            email=request.session["email"]
            useremail = request.session["email"]
            
            try:
                user = Userinfo.objects.get(email=email)
            except:
                return render(request,"login.html",{}) 
            else:
              
                joiningtime = str((user.joining))
                joiningtime = joiningtime[0:11]
                print("joining date : ",joiningtime)

                post = userpost.objects.filter(user_id=user)
                
                user = Userinfo.objects.get(email = useremail)
    
                datass = followers.objects.filter(user_id=user)
                new = []
                new1 = []
                for i in datass:
                    new.append(i.frinds)
                print(new)
                for x in new:
                    myfriends = Userinfo.objects.get(id = x)
                    print(str(myfriends))
                    new1.append(myfriends)
                print(new1)
                size = len(new1)

                suggetion_for_you = []
                
                alluser = Userinfo.objects.all()
                print("All user:-",alluser)
                for i in alluser:
                    print(i.email)
                    print(i)
                    if(str(i.email) == useremail) or (i in new1):
                        print("********")
                        continue
                    else:
                        suggetion_for_you.append(i)
                return render(request,"home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":suggetion_for_you,"size":size})
        else:
            user.save()
            email=request.session["email"]
            useremail = request.session["email"]
            
            try:
                user = Userinfo.objects.get(email=email)
            except:
                return render(request,"login.html",{}) 
            else:
              
                joiningtime = str((user.joining))
                joiningtime = joiningtime[0:11]
                print("joining date : ",joiningtime)

                post = userpost.objects.filter(user_id=user)
                
                user = Userinfo.objects.get(email = useremail)
    
                datass = followers.objects.filter(user_id=user)
                new = []
                new1 = []
                for i in datass:
                    new.append(i.frinds)
                print(new)
                for x in new:
                    myfriends = Userinfo.objects.get(id = x)
                    print(str(myfriends))
                    new1.append(myfriends)
                print(new1)
                size = len(new1)

                suggetion_for_you = []
                
                alluser = Userinfo.objects.all()
                print("All user:-",alluser)
                for i in alluser:
                    print(i.email)
                    print(i)
                    if(str(i.email) == useremail) or (i in new1):
                        print("********")
                        continue
                    else:
                        suggetion_for_you.append(i)
                return render(request,"home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":suggetion_for_you,"size":size})
        # else:
        #     return redirect(home)
            



    '''if "email" in request.session:
        useremail = request.session["email"]
        user = Userinfo.objects.get(email =useremail)
        user_post = userpost.objects.filter(user_id=user)
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        
        #user1 = Userinfo.objects.get(id =id)
        f1 = followers()
        f1.user = user
        f1.frinds = id
        f1.save()
        user = Userinfo.objects.get(id =id)

        datas = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datas:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        


        return render(request,"following.html",{"user":user,"all":suggetion_for_you,"data":user_post,"datas":new1,"size":size,"joiningtime":joiningtime})
        #following = followers.objects.flter(email = useremail)'''
        


   


