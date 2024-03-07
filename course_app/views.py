
from django.shortcuts import render,redirect
import uuid
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from course_app.models import register,courseInfo,payment,userdetails
import bcrypt
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
import random 
import threading


def main(request):
    return render(request,'main2.html')

def course(request):
    return render(request,'course2.html')




def learning(request,token):
    if 'logged_in' in request.session:
        return render(request,'learning.html')


def user(request,token):

    if 'logged_in' in request.session:
     
        if 'user_id' in request.session and request.session.get('user_token')==token:
            user_id = request.session['user_id']
            existing_user = register.objects.get(id=user_id)
            email = existing_user.email
            username=existing_user.username
       
            
            if payment.objects.filter(email=email).exists():
                coursedata = payment.objects.filter(email=email)
                coursedetail = []
                for course in coursedata:
                    coursedetail.append(courseInfo.objects.get(course_instructor=course.course_instructor, course_name=course.course_name))
                
            #  from django.urls import reverse
                # return redirect(reverse('user', kwargs={'username': request.user.username}))
                return render(request, 'user.html', {'coursedata': coursedetail, 'username': username})
            else:
                return render(request, 'user.html', {'buymsg': 'You Need to Buy course'})
        else:
            return render(request, 'login.html', {'msg': 'User ID not found in session.'})
    else:
        return render(request, 'login.html', {'msg': 'User not logged in.'})




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        try:
            existing_user = register.objects.get(username=username, email=email)
            user_password_hash = existing_user.password.encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), user_password_hash):
          
                request.session['logged_in'] = True
                
                request.session['user_token'] = str(uuid.uuid4())
                request.session['user_id'] = existing_user.id  
                return redirect('/user/' + request.session['user_token'])  
            else:
                return render(request, 'login.html', {'msg': 'Invalid credentials'})
        except ObjectDoesNotExist:
            return render(request, 'signin.html', {'msg': 'User not found. Please register.'})
        except Exception as e:
            return render(request, 'login.html', {'msg': 'An error occurred: Please try again later'})
         
    return render(request, 'login.html')

def logout(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_id' in request.session:
        del request.session['user_token']
    return redirect('/login')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        cnfrmpass = request.POST.get('confirmpassword')
        
        if password != cnfrmpass:
            return render(request, 'signin.html', {'msg': 'Password and Confirm Password must be the same'})
        else:
            if not register.objects.filter(email=email).exists():
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
                
                register.objects.create(username=username, mobile=mobile, password=hashed_password.decode('utf-8'), email=email)
                
                return render(request, 'login.html', {'msg': 'Account created successfully'})
            else:
                return render(request, 'signin.html', {'msg': 'Account already exists'})

    return render(request, 'signin.html')


def paymentinfo(request):
    if request.method=='POST':
        courseInstructor=request.POST.get('courseInstructor')
        coursePrice=request.POST.get('coursePrice')
        courseImg=request.POST.get('courseImg')
        courseDuration=request.POST.get('courseDuration')
        courseinfo=request.POST.get('courseInfo')
        dateofpurchase=request.POST.get('dateofpurchase')
        dateofexpiry=request.POST.get('dateofexpiry')
        email=request.POST.get('email')
        
        if register.objects.filter(email=email).exists():
            if not payment.objects.filter(email=email,course_instructor=courseInstructor,course_name=courseinfo).exists():
                payment.objects.create(email=email,course_instructor=courseInstructor,course_name=courseinfo,course_amount=coursePrice,dateofexpiry=dateofexpiry,dateofpurchase=dateofpurchase)

                # mail
                invoice_data = {
                    'courseInstructor': courseInstructor,
                    'coursePrice': coursePrice,
                    'courseImg': courseImg,
                    'courseDuration': courseDuration,
                    'courseinfo': courseinfo,
                    'dateofpurchase': dateofpurchase,
                    'dateofexpiry': dateofexpiry,
                    'email': email,
                }
                invoice_html=render_to_string('invoice.html',invoice_data)
                subject = "Successful Payment"
                message = f"Hi, welcome to the family of Scale Academy. You have successfully purchased {courseinfo}."
                from_mail = 'krishrchitroda1@gmail.com'
                recipient_list = [f'{email}']
                # html = f"<html> Hi, welcome to the family of aptech. You have successfully purchased {courseinfo}. <h4>Click on the login button for login.</h4> <button><a href='https://bri12.pythonanywhere.com/'>Login</a></button></html>"

                msg = EmailMultiAlternatives(subject, message, from_mail, recipient_list)
                msg.attach_alternative(invoice_html, "text/html")
                msg.send()
                

            else:
                return render(request,'course2.html',{'msg':'Course has been already bought'})
            if not courseInfo.objects.filter(course_instructor=courseInstructor,course_name=courseinfo).exists():
                courseInfo.objects.create(course_instructor=courseInstructor,course_name=courseinfo,course_Img=courseImg,course_duration=courseDuration,course_amount=coursePrice) 
            return render(request,'login.html',{'msg':'Course has been brought successfully'})

        else:
            return render(request,'login.html',{'msg':'You need to register/SignIn'})
    return render(request,'payment.html')

def otpgenerate(request):
    if request.method=='POST':
        emailforotp=request.POST.get('email')
        
        if register.objects.filter(email=emailforotp).exists():
            global otp_gen 
            otp_gen=random.randint(100000,999999)
            subject = "OTP"
            message = f"{otp_gen}"
            from_mail = 'krishrchitroda1@gmail.com'
            recipient_list = [f'{emailforotp}']
            msg = EmailMultiAlternatives(subject, message, from_mail, recipient_list)
            msg.send()
            return render(request,'update.html',{'email':emailforotp})
        else:
            return render(request,'login.html',{'msg':'user does not exist please register'})


    return render(request,'otpverify.html')

def update_(request):
    if request.method=='POST':
        password=request.POST.get('password')
        email=request.POST.get('email')
        repeatpass=request.POST.get('repeatpassword')
        otp=request.POST.get('otp')
        if int(otp_gen)==int(otp):
            if password==repeatpass:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                try:
                    user = register.objects.get(email=email)
                    user.password = hashed_password.decode('utf-8')
                    user.save()
                    return render(request, 'login.html', {'msg': 'Password has been successfully updated'})
                except register.DoesNotExist:
                    return render(request, 'login.html', {'msg': 'User with this email does not exist'})
            else:
                return render(request, 'update.html', {"msg": 'password and repeatpassword should be same'})
        else:
            return render(request, 'login.html', {"msg": "wrong otp"})
    return render(request, 'update.html')


    

def userdetail(request):
    if 'logged_in' in request.session:
        user_id = request.session['user_id']
        existing_user = register.objects.get(id=user_id)
        email = existing_user.email
        username=existing_user.username
        mobile=existing_user.mobile
        detail={'email':email,'username':username,'mobile':mobile}

        if request.method=='POST':
        
            firstname=request.POST.get('firstname')
        
            lastname=request.POST.get('lastname')
            gender=request.POST.get('gender')

            if 'img' in request.FILES:
                myfile = request.FILES['img']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                image = fs.url(filename)
            elif not userdetails.objects.filter(email=email).exists():
                image=None
            else:
                use_r=userdetails.objects.get(email=email)
                image=use_r.img
            profession=request.POST.get('profession')
            
            detail={'email':email,'username':username,'mobile':mobile,'firstname':firstname,'lastname':lastname,'gender':gender,'img':image,'profession':profession,'msg':'changed has been updated please refresh'}

            if not userdetails.objects.filter(email=email).exists():
                userdetails.objects.create(email=email,firstname=firstname,lastname=lastname,gender=gender,mobile=mobile,profession=profession,img=image)
                return render(request,'userdetails.html',detail)
            else:
                user_detail=userdetails.objects.get(email=email)
                user_detail.profession=profession
                user_detail.img=image
                user_detail.firstname=firstname
                user_detail.lastname=lastname
                user_detail.gender=gender
                user_detail.save()
                return render(request,'userdetails.html',detail)

        
        if userdetails.objects.filter(email=email).exists():
            user=userdetails.objects.get(email=email)
            
            detail={'email':email,'username':username,'mobile':mobile,'firstname':user.firstname,'lastname':user.lastname,'gender':user.gender,'img':user.img,'profession':user.profession}
        return render(request,'userdetails.html',detail)
    



    
