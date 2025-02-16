from django.shortcuts import render,redirect
from.models import student,faculty,candidate,nomination,notification
from django.contrib import messages
def reg(request):
 if request.method=="POST":
     name=request.POST.get('name')
     phoneno=request.POST.get('phoneno')
     email=request.POST.get('email')
     password=request.POST.get('password')
     registerno=request.POST.get('registerno')
     course=request.POST.get('course')
     department=request.POST.get('department')
     student(name=name,phoneno=phoneno,email=email,password=password,registerno=registerno,course=course,department=department).save()
     return render(request, 'reg.html', {'success': True})
    
 else:
   return render(request, 'reg.html', {'success': False})
 
def facultyreg(request):
  if request.method=="POST":
     facultyid=request.POST.get('facultyid')
     password=request.POST.get('password')
     name=request.POST.get('name')
     phoneno=request.POST.get('phoneno')
     email=request.POST.get('email')
     department=request.POST.get('department')
     faculty(facultyid=facultyid,password=password,name=name,phoneno=phoneno,email=email,department=department).save()

     return render(request,'index.html')
  else:
      return render(request,'facultyreg.html') 
    
# Create your views here.
def index(request):
    return render(request,'index.html') 

def dupliindex2(request):
    return render(request,'dupliindex2.html')
def faculty2(request):
    return render(request,'faculty2.html')

#login page
def candidatelogin(request):
    if request.method=='POST':
        candidateid=request.POST.get('candidateid')
        p=request.POST.get('password')
        data=candidate.objects.filter(candidateid=candidateid,password=p)
        if(data.exists()):
            request.session['candidateid']=candidateid
            return render(request,'candidatehome.html')
        else:
            return render(request,'candidatelogin.html')
    else:
        return render(request,'candidatelogin.html')
def candidatehome(request):
    return render(request,'candidatehome.html')


def studentlogin(request):
    if request.method=='POST':
        registerno=request.POST.get('registerno')
        p=request.POST.get('password')
        data=student.objects.filter(registerno=registerno,password=p)
        if(data.exists()):
            request.session['registerno']=registerno
            return render(request,'studenthome.html')
        else:
            messages.error(request, 'Invalid registration number or password.')
            return render(request,'studentlogin.html')
    else:
        return render(request,'studentlogin.html')
def studenthome(request):
    return render(request,'studenthome.html')     
def facultylogin(request):
    if request.method=='POST':
        facultyid=request.POST.get('facultyid')
        p=request.POST.get('password')
        data=faculty.objects.filter(facultyid=facultyid,password=p)
        if(data.exists()):
            request.session['facultyid']=facultyid
            return render(request,'facultyhome.html')
        else:
            
            return render(request,'facultylogin.html')
    else:
        return render(request,'facultylogin.html')  
def facultyhome(request):
    return render(request,'facultyhome.html')              
def adminlogin(request):
    if request.method=='POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        u='admin'
        p='password'
        if name==u:
            if password==p:
                return redirect('adminhome')
            else:
                return render(request,'adminlogin.html')
        else:
            return render(request,'adminlogin.html') 
    return render(request,'adminlogin.html')    
def adminhome(request):
    return render(request,'adminhome.html')
def profile(request):
    registerno=request.session.get('registerno')
    
    if registerno:
        user= student.objects.get(registerno=registerno)
        return render(request,'profile.html',{'user':user})
    else:
        return redirect('studentlogin')    
    
def logout(request):
    request.session.flush()
    return redirect('index')
def editprofile(request):
    if request.method=='POST':
        registerno=request.session.get('registerno')
        user=student.objects.get(registerno=registerno)
        name=request.POST.get('name')
        
        phoneno=request.POST.get('phoneno')
        email=request.POST.get('email')
        course=request.POST.get('course')
        department=request.POST.get('department')
        user.name=name
        user.phoneno=phoneno
        user.email=email
        user.course=course
        user.department=department
      
        user.save()
        return redirect('profile')
    return render(request,'profile.html')



from django.shortcuts import render, redirect

from .models import nomination, faculty
from django.contrib import messages


def candidatereg(request):
    studentreg = request.session.get('registerno')  # Assuming 'student' is linked to 'user'
    
    if request.method == "POST":
        # Check if the registration number already exists in the Nomination table
        regno = request.POST.get('regno')
        if nomination.objects.filter(regno=regno).exists():
            return render(request, 'candidatereg.html', {'successful': False, 'message': 'Application already submitted for this registration number.'})

        # Retrieve selected faculty member from the form
        tutor_in_charge =faculty.objects.get(facultyid=request.POST.get('tutor_in_charge'))
        student_instance = student.objects.get(registerno=studentreg)
        # Save the nomination record
        new_nomination = nomination(
            studentid=student_instance,  # This links the student to the nomination
            tutor_in_charge=tutor_in_charge,
            name=request.POST.get('name'),
            phoneno=request.POST.get('phoneno'),
            email=request.POST.get('email'),
            regno=request.POST.get('regno'),
            department=request.POST.get('department'),
            course=request.POST.get('course'),
            year=request.POST.get('year'),
            attendance=request.POST.get('attendance'),
            backlog=request.POST.get('backlog'),
            position=request.POST.get('position')
        )
        new_nomination.save()

       
        return render(request,'candidatereg.html',{'successful': True,'message': 'Nomination submitted successfully! Further updates will get through email.'})  # Redirect to avoid form resubmission after refresh
    else:
        # Fetch all available faculties
        faculties = faculty.objects.all()
        return render(request, 'candidatereg.html', {'faculties': faculties, 'successful': False})


def userlist(request):
    user=student.objects.all()
    return render(request,'userlist.html',{'user':user})

def deleteuser(request,id):
    data=student.objects.filter(id=id)
    data.delete()
    return redirect ('userlist')

def nominationlist(request):
    facultyid = request.session.get('facultyid')
    user = None  # Initialize the user variable

    if facultyid:
        # Fetch the student object based on the registerno from the session
        user1 = faculty.objects.get(facultyid=facultyid)

        # Filter nominations based on the department of the user1
        user = nomination.objects.filter(department=user1.department).order_by('-created_at')

    # Render the template with the filtered nominations
    return render(request, 'nominationlist.html', {'user': user})

def deletenomination(request,id):
    data=nomination.objects.filter(id=id)
    data.delete()
    return redirect ('nominationlist')

def update_status(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        status=request.POST.get('status')

        if not email or not status:
            return redirect('nominationlist')
        if status not in ['applied','approved','rejected']:
            return redirect('nominationlist')
        constr = get_object_or_404(nomination, email==email) # type: ignore
        constr.status = status
        constr.save()
    return redirect('nominationlist')


def candidatelist(request):
    data=candidate.objects.all()
    return render(request,'candidatelist.html',{'data':data})

def deletecandidate(request,id):
    data=candidate.objects.filter(id=id)
    data.delete()
    return redirect ('candidatelist')

def facultylist(request):
    fac=faculty.objects.all()
    return render(request,'facultylist.html',{'fac':fac})

def deletefaculty(request,id):
    data=faculty.objects.filter(id=id)
    data.delete()
    return redirect ('facultylist')

def facultyprofile(request):
    facultyid=request.session.get('facultyid')
    if facultyid:
        user= faculty.objects.get(facultyid=facultyid)
        return render(request,'facultyprofile.html',{'user':user})
    else:
        return redirect('login')     

def facultyeditprofile(request):
    if request.method=='POST':
        facultyid=request.session.get('facultyid')
        
        user=faculty.objects.get(facultyid=facultyid)
        name=request.POST.get('name')
        phoneno=request.POST.get('phoneno')
        email=request.POST.get('email')
        department=request.POST.get('department')
        user.name=name
        user.phoneno=phoneno
        user.email=email
        user.department=department
      
        user.save()
        return redirect('facultyprofile')
    return render(request,'facultyprofile.html')  

def candidateprofile(request):
    candidateid=request.session.get('candidateid')
    if candidateid:
        user=candidate.objects.get(candidateid=candidateid)
        return render(request,'candidateprofile.html',{'user':user})
    else:
        return redirect('login')  
        
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

def changepassword(request):
    if request.method == 'POST':
        # Step 1: Submit email and send OTP
        if 'email' in request.POST and not request.session.get('otp_sent', False):
            email = request.POST.get('email')
            if email:
                # Generate OTP
                otp = generate_otp()
                # Store OTP in session
                request.session['otp'] = otp
                request.session['email'] = email
                request.session['otp_sent'] = True
                
                # Send OTP email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is: {otp}',
                    settings.EMAIL_HOST_USER,  # Sender's email (configured in settings.py)
                    [email],  # Recipient's email
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email address! Check your inbox.')
                return render(request, 'changepassword.html', {'email': email})
            else:
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'changepassword.html')

        # Step 2: Verify OTP
        if 'otp' in request.POST and request.session.get('otp_sent', False):
            entered_otp = request.POST.get('otp')
            stored_otp = request.session.get('otp')
            
            if entered_otp == stored_otp:
                # OTP is correct, user can change the password
                messages.success(request, 'OTP verified successfully! You can now change your password.')
                # Redirect to the password change page (implement password change view)
                return redirect('resetpassword')  # Replace 'change_password' with your password change URL
            else:
                messages.error(request, 'Invalid OTP. Please try again.')

    # If no OTP has been sent, render the form to input email
    return render(request, 'changepassword.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def resetpassword(request):
    if request.method == 'POST':
        # Get the new password and confirm password from the form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            # Passwords don't match
            messages.error(request, "Passwords do not match.")
            return render(request, 'resetpassword.html')

        # If passwords match, proceed to reset the password
        user = candidate.objects.get(candidateid=request.session.get('email'))  # Assuming email is stored in session
        user.password = new_password
        user.save()

        messages.success(request, "Your password has been successfully reset!")
        return redirect('candidatelogin')  # Redirect to login page after password reset
    return render(request, 'resetpassword.html')

def forgotpassword(request):
    if request.method=='POST':

        registerno=request.POST.get('registerno')
        user=student.objects.get(registerno=registerno)
        password=request.POST.get('password')
        user.password=password
        user.save()
        return redirect('studentlogin')
    else:
        return render(request,'forgotpassword.html')    

def candidateeditprofile(request):
    if request.method=='POST':
        candidateid=request.session.get('candidateid')
        user=candidate.objects.get(candidateid=candidateid)
        name=request.POST.get('name')
        
        department=request.POST.get('department')
        course=request.POST.get('course')
        policy1=request.POST.get('policy1')
        policy2=request.POST.get('policy2')
        policy3=request.POST.get('policy3')
        avatar=request.FILES.get('avatar')
        user.name=name
        
        user.department=department
        user.course=course
        user.policy1=policy1
        user.policy2=policy2
        user.policy3=policy3
        if avatar:
            user.avatar=avatar
        user.save()
        return redirect('candidateprofile')
    return render(request,'candidateprofile.html')

      
def candidateview(request):
    data=candidate.objects.all().order_by('position') 
    return render(request,'candidateview.html',{'data':data})    

def fcandidateview(request):
    data=candidate.objects.all().order_by('position') 
    return render(request,'fcandidateview.html',{'data':data})    

def c_candidateview(request):
    data=candidate.objects.all().order_by('position') 
    return render(request,'c_candidateview.html',{'data':data}) 

#chat section

from .models import Room, Message

# Create your views here.


def HomeView(request):
    if request.method == "POST":
        username = request.POST["username"]
        room = request.POST["room"]
        try:
            existing_room = Room.objects.get(room_name__icontains=room)
        except Room.DoesNotExist:
            r = Room.objects.create(room_name=room)
        return redirect("room", room_name=room, username=username)
    return render(request, "home.html")


def RoomView(request, room_name, username):
    try:
        existing_room = Room.objects.get(room_name__icontains=room_name)
    except Room.DoesNotExist:
        return redirect("chat")
    get_messages = Message.objects.filter(room=existing_room)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": existing_room.room_name,
    }

    return render(request, "room.html", context)

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import nomination,Vote

def update_nomination(request, nomination_id):
    # Get the nomination object by ID
    nomini = nomination.objects.get(id=nomination_id)

    if request.method == 'POST':
        # Get the new status from the form submission
        new_status = request.POST.get('status')
        reason=request.POST.get('reason')
        
        # Update the status of the nomination
        nomini.status = new_status
        nomini.reason=reason
        nomini.save()

        # Prepare the email content
        # subject = f'Your nomination status: {new_status}'
        # message = (
        #     f"Dear {nomini.name},\n\n"
        #     f"Congratulations! Your nomination has been {new_status}.\n\n"
        #     f"Nomination details:\n"
        #     f"Nomination Name: {nomini.name}\n"
        #     f"Nomination Email: {nomini.email}\n"
        #     f"Your Login Password is: {nomini.regno}\n"
        # )

        # # Email details
        # from_email = 'elected2004@gmail.com'
        # recipient_list = [nomini.email]

        # try:
        #     # Send the email
        #     send_mail(subject, message, from_email, recipient_list)
        # except Exception as e:
        #     print(f"Error Sending email: {e}")

        # Redirect to the nomination list after successful status update
        return redirect('nominationlist')

    # If it's a GET request, render the nomination page
    return render(request, 'nominationlist.html', {'nomini': nomini})


def nominationapproved(request):
    data=nomination.objects.all().order_by('-created_at')
    return render(request, 'approved_nominations.html', {'data': data})
# def approved_nominations(request):
#     return render(request,'approved_nominations.html')
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse


def sendemail(request, nomination_id):
    nomini = nomination.objects.get(id=nomination_id)

    if request.method == 'POST':
        # Prepare the email content
        if nomini.status == 'approved':
            subject = f'Congratulations! Your nomination status: {nomini.status}'
            message = (
                f"Dear {nomini.name},\n\n"
                f"Congratulations! Your nomination has been {nomini.status}.\n\n"
                f"Login details:\n"
                f"Login Email: {nomini.email}\n"
                f"password:If you are logging in first time,please follow the below steps to reset your password:\n"
                f"1.Open portal login page\n"
                f"2.Click on forgot password\n"
                f"3.Enter your Login Emial\n"
                f"4.Generate OTP\n"
                f"5.Create a new password and login to the portal"
            )
        elif nomini.status == 'rejected':
            subject = f'Sorry, your nomination status: {nomini.status}'
            message = (
                f"Dear {nomini.name},\n\n"
                f"We regret to inform you that your nomination has been {nomini.status} due to {nomini.reason}\n\n"
                f"Nomination details:\n"
                f"Nomination Name: {nomini.name}\n"
              
            )

        # Save candidate information
        candidate(password=nomini.regno, name=nomini.name, candidateid=nomini.email, 
                  position=nomini.position, course=nomini.course, department=nomini.department).save()
        
        # Email details
        from_email = 'elected2004@gmail.com'
        recipient_list = [nomini.email]

        try:
            # Send the email
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Error Sending email: {e}")

        # Redirect to the nomination list after successful status update
        return redirect('approved_nominations')

    # If it's a GET request, render the nomination page
    return render(request, 'approved_nominations.html', {'nomini': nomini})


def vote(request):
    # Fetch candidates from the database for each position (you can filter by department, etc., if needed)
    chairperson = candidate.objects.filter(position='Chairperson') 
    vicechairperson = candidate.objects.filter(position='Vice Chairperson')
    generalsecretary= candidate.objects.filter(position='General Secretary')   
    jointsecretary = candidate.objects.filter(position='Joint Secretary')
    finearts = candidate.objects.filter(position='Fine Arts Secretary') 
    studenteditor = candidate.objects.filter(position='Student Editor')  # Example: You can filter by position if necessary
    uuc1 = candidate.objects.filter(position='UUC')
    uuc2 = candidate.objects.filter(position='UUC') 
    # Fetch other candidates (Secretary, Student Council, etc.) similarly
    return render(request, 'vote.html', {
        'chairperson': chairperson,
        'vicechairperson':vicechairperson,
        'generalsecretary':generalsecretary,
        'jointsecretary':jointsecretary,
        'finearts':finearts,
        'studenteditor':studenteditor,
        'uuc1':uuc1,
        'uuc2':uuc2,
    })


# def vote_page(request):
#     # Retrieve all the candidates for each position
#     chairperson_candidates = candidate.objects.filter(position='chairperson')
#     vice_chairperson_candidates = candidate.objects.filter(position='vicechairperson')
#     general_secretary_candidates = candidate.objects.filter(position='generalsecretary')
#     joint_secretary_candidates = candidate.objects.filter(position='jointsecretary')
#     fine_arts_candidates = candidate.objects.filter(position='finearts')
#     student_editor_candidates = candidate.objects.filter(position='studenteditor')
#     uuc_rep_1_candidates = candidate.objects.filter(position='uuc1')
#     uuc_rep_2_candidates = candidate.objects.filter(position='uuc2')

#     # Handle form submission
#     if request.method == 'POST':
#         registerno=request.session.get('registerno')
#         if registerno:
#             user= student.objects.get(registerno=registerno)
#         # Create or update the user's vote
#         vote, created = Vote.objects.get_or_create(user=user)

#         # Get the selected candidates from the form data
#         vote.chairperson = candidate.objects.get(candidateid=request.POST.get('chairperson'))
#         vote.vice_chairperson = candidate.objects.get(candidateid=request.POST.get('vicechairperson'))
#         vote.general_secretary = candidate.objects.get(candidateid=request.POST.get('generalsecretary'))
#         vote.joint_secretary = candidate.objects.get(candidateid=request.POST.get('jointsecretary'))
#         vote.fine_arts_secretary = candidate.objects.get(candidateid=request.POST.get('finearts'))
#         vote.student_editor = candidate.objects.get(candidateid=request.POST.get('studenteditor'))
#         vote.uuc_rep_1 = candidate.objects.get(candidateid=request.POST.get('uuc1'))
#         vote.uuc_rep_2 = candidate.objects.get(candidateid=request.POST.get('uuc2'))

#         # Save the vote
#         vote.save()

#         return redirect('index')  # Redirect to a thank-you page after submission

#     return render(request, 'vote.html', {
#         'chairperson': chairperson_candidates,
#         'vicechairperson': vice_chairperson_candidates,
#         'generalsecretary': general_secretary_candidates,
#         'jointsecretary': joint_secretary_candidates,
#         'finearts': fine_arts_candidates,
#         'studenteditor': student_editor_candidates,
#         'uuc1': uuc_rep_1_candidates,
#         'uuc2': uuc_rep_2_candidates,
#     })

def vote_page(request):
    # Retrieve all the candidates for each position
    chairperson_candidates = candidate.objects.filter(position='Chairperson')
    vice_chairperson_candidates = candidate.objects.filter(position='Vice Chairperson')
    general_secretary_candidates = candidate.objects.filter(position='General Secretary')
    joint_secretary_candidates = candidate.objects.filter(position='Joint Secretary')
    fine_arts_candidates = candidate.objects.filter(position='Fine Arts Secretary')
    student_editor_candidates = candidate.objects.filter(position='Student Editor')
    uuc_rep_1_candidates = candidate.objects.filter(position='UUC')
    uuc_rep_2_candidates = candidate.objects.filter(position='UUC')

    # Handle form submission
    if request.method == 'POST':
        registerno = request.session.get('registerno')
        if registerno:
            user = student.objects.get(registerno=registerno)
        # Create or update the user's vote
        vote, created = Vote.objects.get_or_create(user=user)

        # Fetch the selected candidates from form data
        chairperson_vote = request.POST.get('chairperson')
        vice_chairperson_vote = request.POST.get('vice_chairperson')
        general_secretary_vote = request.POST.get('general_secretary')
        joint_secretary_vote = request.POST.get('joint_secretary')
        fine_arts_secretary_vote = request.POST.get('fine_arts_secretary')
        student_editor_vote = request.POST.get('student_editor')
        uuc_rep_1_vote = request.POST.get('uuc_rep_1')
        uuc_rep_2_vote = request.POST.get('uuc_rep_2')

        # If the user selects NOTA, the value would be 'none'
        if chairperson_vote != 'none':
            vote.chairperson = candidate.objects.get(candidateid=chairperson_vote)
        if vice_chairperson_vote != 'none':
            vote.vice_chairperson = candidate.objects.get(candidateid=vice_chairperson_vote)
        if general_secretary_vote != 'none':
            vote.general_secretary = candidate.objects.get(candidateid=general_secretary_vote)
        if joint_secretary_vote != 'none':
            vote.joint_secretary = candidate.objects.get(candidateid=joint_secretary_vote)
        if fine_arts_secretary_vote != 'none':
            vote.fine_arts_secretary = candidate.objects.get(candidateid=fine_arts_secretary_vote)
        if student_editor_vote != 'none':
            vote.student_editor = candidate.objects.get(candidateid=student_editor_vote)
        if uuc_rep_1_vote != 'none':
            vote.uuc_rep_1 = candidate.objects.get(candidateid=uuc_rep_1_vote)
        if uuc_rep_2_vote != 'none':
            vote.uuc_rep_2 = candidate.objects.get(candidateid=uuc_rep_2_vote)

        # Save the vote
        vote.save()

        return redirect('vote')  # Redirect to a thank-you page after submission

    return render(request, 'vote.html', {
        'chairperson': chairperson_candidates,
        'vicechairperson': vice_chairperson_candidates,
        'generalsecretary': general_secretary_candidates,
        'jointsecretary': joint_secretary_candidates,
        'finearts': fine_arts_candidates,
        'studenteditor': student_editor_candidates,
        'uuc1': uuc_rep_1_candidates,
        'uuc2': uuc_rep_2_candidates,
    })




def csnominationlist(request):
    user=nomination.objects.filter(department='Computer Science').order_by('-created_at')
    return render(request,'nominationlist.html',{'user':user})

def result(request):
    return render(request,'result.html')

def fresult(request):
    return render(request,'fresults.html')
def cresult(request):
    return render(request,'cresults.html')    



from django.shortcuts import render
from django.db.models import Count, F, Q
from .models import Vote, candidate

def election_results(request):
    # Aggregate votes for each position
    chairperson_results = candidate.objects.filter(chairperson_votes__isnull=False).annotate(total_votes=Count('chairperson_votes'))
    vicechairperson_results = candidate.objects.filter(vice_chairperson_votes__isnull=False).annotate(total_votes=Count('vice_chairperson_votes'))
    generalsecretary_results = candidate.objects.filter(general_secretary_votes__isnull=False).annotate(total_votes=Count('general_secretary_votes'))
    jointsecretary_results = candidate.objects.filter(joint_secretary_votes__isnull=False).annotate(total_votes=Count('joint_secretary_votes'))
    finearts_results = candidate.objects.filter(fine_arts_secretary_votes__isnull=False).annotate(total_votes=Count('fine_arts_secretary_votes'))
    studenteditor_results = candidate.objects.filter(student_editor_votes__isnull=False).annotate(total_votes=Count('student_editor_votes'))

    # Aggregate votes for UUCR candidates (both uuc_rep_1 and uuc_rep_2)
    uuc_combined_results = candidate.objects.annotate(
        total_uuc_rep_1_votes=Count('uuc_rep_1_votes', distinct=True),
        total_uuc_rep_2_votes=Count('uuc_rep_2_votes', distinct=True),
        total_votes=F('total_uuc_rep_1_votes') + F('total_uuc_rep_2_votes')
    ).filter(
        Q(uuc_rep_1_votes__isnull=False) | Q(uuc_rep_2_votes__isnull=False)  # Using Q object to combine conditions
    ).order_by('-total_votes')

    # Get top 2 winners for UUCR based on total votes
    uuc_winners = uuc_combined_results[:2]

    # Context to pass the results
    context = {
        "chairperson_results": chairperson_results,
        "vicechairperson_results": vicechairperson_results,
        "generalsecretary_results": generalsecretary_results,
        "jointsecretary_results": jointsecretary_results,
        "finearts_results": finearts_results,
        "studenteditor_results": studenteditor_results,
        "uuc_combined_results": uuc_combined_results,
        "uuc_winners": uuc_winners,
    }

    # Get the position to display based on the button click
    position = request.GET.get('position', '')

    # Filter winners based on position
    winners = {}
    if position == 'chairperson':
        winners = sorted(chairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'vicechairperson':
        winners = sorted(vicechairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'generalsecretary':
        winners = sorted(generalsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'jointsecretary':
        winners = sorted(jointsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'finearts':
        winners = sorted(finearts_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'studenteditor':
        winners = sorted(studenteditor_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'uuc':
        winners = uuc_winners

    context['position'] = position
    context['winners'] = winners

    return render(request, "results.html", context)


def felection_results(request):
    # Aggregate votes for each position
    chairperson_results = candidate.objects.filter(chairperson_votes__isnull=False).annotate(total_votes=Count('chairperson_votes'))
    vicechairperson_results = candidate.objects.filter(vice_chairperson_votes__isnull=False).annotate(total_votes=Count('vice_chairperson_votes'))
    generalsecretary_results = candidate.objects.filter(general_secretary_votes__isnull=False).annotate(total_votes=Count('general_secretary_votes'))
    jointsecretary_results = candidate.objects.filter(joint_secretary_votes__isnull=False).annotate(total_votes=Count('joint_secretary_votes'))
    finearts_results = candidate.objects.filter(fine_arts_secretary_votes__isnull=False).annotate(total_votes=Count('fine_arts_secretary_votes'))
    studenteditor_results = candidate.objects.filter(student_editor_votes__isnull=False).annotate(total_votes=Count('student_editor_votes'))

    # Aggregate votes for UUCR candidates (both uuc_rep_1 and uuc_rep_2)
    uuc_combined_results = candidate.objects.annotate(
        total_uuc_rep_1_votes=Count('uuc_rep_1_votes', distinct=True),
        total_uuc_rep_2_votes=Count('uuc_rep_2_votes', distinct=True),
        total_votes=F('total_uuc_rep_1_votes') + F('total_uuc_rep_2_votes')
    ).filter(
        Q(uuc_rep_1_votes__isnull=False) | Q(uuc_rep_2_votes__isnull=False)  # Using Q object to combine conditions
    ).order_by('-total_votes')

    # Get top 2 winners for UUCR based on total votes
    uuc_winners = uuc_combined_results[:2]

    # Context to pass the results
    context = {
        "chairperson_results": chairperson_results,
        "vicechairperson_results": vicechairperson_results,
        "generalsecretary_results": generalsecretary_results,
        "jointsecretary_results": jointsecretary_results,
        "finearts_results": finearts_results,
        "studenteditor_results": studenteditor_results,
        "uuc_combined_results": uuc_combined_results,
        "uuc_winners": uuc_winners,
    }

    # Get the position to display based on the button click
    position = request.GET.get('position', '')

    # Filter winners based on position
    winners = {}
    if position == 'chairperson':
        winners = sorted(chairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'vicechairperson':
        winners = sorted(vicechairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'generalsecretary':
        winners = sorted(generalsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'jointsecretary':
        winners = sorted(jointsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'finearts':
        winners = sorted(finearts_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'studenteditor':
        winners = sorted(studenteditor_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'uuc':
        winners = uuc_winners

    context['position'] = position
    context['winners'] = winners

    return render(request, "fresults.html", context)

def celection_results(request):
    # Aggregate votes for each position
    chairperson_results = candidate.objects.filter(chairperson_votes__isnull=False).annotate(total_votes=Count('chairperson_votes'))
    vicechairperson_results = candidate.objects.filter(vice_chairperson_votes__isnull=False).annotate(total_votes=Count('vice_chairperson_votes'))
    generalsecretary_results = candidate.objects.filter(general_secretary_votes__isnull=False).annotate(total_votes=Count('general_secretary_votes'))
    jointsecretary_results = candidate.objects.filter(joint_secretary_votes__isnull=False).annotate(total_votes=Count('joint_secretary_votes'))
    finearts_results = candidate.objects.filter(fine_arts_secretary_votes__isnull=False).annotate(total_votes=Count('fine_arts_secretary_votes'))
    studenteditor_results = candidate.objects.filter(student_editor_votes__isnull=False).annotate(total_votes=Count('student_editor_votes'))

    # Aggregate votes for UUCR candidates (both uuc_rep_1 and uuc_rep_2)
    uuc_combined_results = candidate.objects.annotate(
        total_uuc_rep_1_votes=Count('uuc_rep_1_votes', distinct=True),
        total_uuc_rep_2_votes=Count('uuc_rep_2_votes', distinct=True),
        total_votes=F('total_uuc_rep_1_votes') + F('total_uuc_rep_2_votes')
    ).filter(
        Q(uuc_rep_1_votes__isnull=False) | Q(uuc_rep_2_votes__isnull=False)  # Using Q object to combine conditions
    ).order_by('-total_votes')

    # Get top 2 winners for UUCR based on total votes
    uuc_winners = uuc_combined_results[:2]

    # Context to pass the results
    context = {
        "chairperson_results": chairperson_results,
        "vicechairperson_results": vicechairperson_results,
        "generalsecretary_results": generalsecretary_results,
        "jointsecretary_results": jointsecretary_results,
        "finearts_results": finearts_results,
        "studenteditor_results": studenteditor_results,
        "uuc_combined_results": uuc_combined_results,
        "uuc_winners": uuc_winners,
    }

    # Get the position to display based on the button click
    position = request.GET.get('position', '')

    # Filter winners based on position
    winners = {}
    if position == 'chairperson':
        winners = sorted(chairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'vicechairperson':
        winners = sorted(vicechairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'generalsecretary':
        winners = sorted(generalsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'jointsecretary':
        winners = sorted(jointsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'finearts':
        winners = sorted(finearts_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'studenteditor':
        winners = sorted(studenteditor_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'uuc':
        winners = uuc_winners

    context['position'] = position
    context['winners'] = winners

    return render(request, "cresults.html", context)
 
def aelection_results(request):
    # Aggregate votes for each position
    chairperson_results = candidate.objects.filter(chairperson_votes__isnull=False).annotate(total_votes=Count('chairperson_votes'))
    vicechairperson_results = candidate.objects.filter(vice_chairperson_votes__isnull=False).annotate(total_votes=Count('vice_chairperson_votes'))
    generalsecretary_results = candidate.objects.filter(general_secretary_votes__isnull=False).annotate(total_votes=Count('general_secretary_votes'))
    jointsecretary_results = candidate.objects.filter(joint_secretary_votes__isnull=False).annotate(total_votes=Count('joint_secretary_votes'))
    finearts_results = candidate.objects.filter(fine_arts_secretary_votes__isnull=False).annotate(total_votes=Count('fine_arts_secretary_votes'))
    studenteditor_results = candidate.objects.filter(student_editor_votes__isnull=False).annotate(total_votes=Count('student_editor_votes'))

    # Aggregate votes for UUCR candidates (both uuc_rep_1 and uuc_rep_2)
    uuc_combined_results = candidate.objects.annotate(
        total_uuc_rep_1_votes=Count('uuc_rep_1_votes', distinct=True),
        total_uuc_rep_2_votes=Count('uuc_rep_2_votes', distinct=True),
        total_votes=F('total_uuc_rep_1_votes') + F('total_uuc_rep_2_votes')
    ).filter(
        Q(uuc_rep_1_votes__isnull=False) | Q(uuc_rep_2_votes__isnull=False)  # Using Q object to combine conditions
    ).order_by('-total_votes')

    # Get top 2 winners for UUCR based on total votes
    uuc_winners = uuc_combined_results[:2]

    # Context to pass the results
    context = {
        "chairperson_results": chairperson_results,
        "vicechairperson_results": vicechairperson_results,
        "generalsecretary_results": generalsecretary_results,
        "jointsecretary_results": jointsecretary_results,
        "finearts_results": finearts_results,
        "studenteditor_results": studenteditor_results,
        "uuc_combined_results": uuc_combined_results,
        "uuc_winners": uuc_winners,
    }

    # Get the position to display based on the button click
    position = request.GET.get('position', '')

    # Filter winners based on position
    winners = {}
    if position == 'chairperson':
        winners = sorted(chairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'vicechairperson':
        winners = sorted(vicechairperson_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'generalsecretary':
        winners = sorted(generalsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'jointsecretary':
        winners = sorted(jointsecretary_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'finearts':
        winners = sorted(finearts_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'studenteditor':
        winners = sorted(studenteditor_results, key=lambda c: c.total_votes, reverse=True)[:1]
    elif position == 'uuc':
        winners = uuc_winners

    context['position'] = position
    context['winners'] = winners

    return render(request, "aresults.html", context) 


def addnotification(request):
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        notification(title=title,description=description).save()

        return redirect('adminhome')
    else:
        return render(request, 'addnotification.html')
        
def viewnotification(request):
    data=notification.objects.all()
    return render(request,'deletenotification.html',{'data':data})

def viewnotifications(request):
    data=notification.objects.all()
    return render(request,'viewnotification.html',{'data':data})

def deletenotification(request,id):
    data=notification.objects.filter(id=id)
    data.delete()
    return redirect ('deletenotification')

from django.shortcuts import render
from .models import candidate, nomination
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# def predict_best_candidate(request):
#     # Load data from models
#     candidates = pd.DataFrame(candidate.objects.all().values())
#     nominations = pd.DataFrame(nomination.objects.all().values())

#     # Merge data on relevant fields (e.g., name, position)
#     data = pd.merge(candidates, nominations, on=['name', 'position'], how='inner')

#     if data.empty:
#         return render(request, "prediction.html", {"error": "No matching data found for candidates and nominations"})

#     # Process attendance as a numeric score
#     data['attendance_score'] = data['attendance'].astype(float)

#     # Handle missing or empty policies
#     model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
#     data['policy_score'] = data.apply(
#         lambda row: np.mean(model.encode(row['policy1'] + " " + row['policy2'] + " " + row['policy3'])) 
#                     if row['policy1'] or row['policy2'] or row['policy3'] else 0,
#         axis=1
#     )

#     # Backlog processing: Penalize candidates with many backlogs
#     data['backlog_score'] = data['backlog'].apply(lambda x: 1 if x.lower() == 'none' else max(0, 1 / (1 + int(x))))

#     # Apply thresholds for disqualification
#     data = data[(data['attendance_score'] >= 75) & (data['backlog_score'] > 0.3)]  # Example thresholds

#     if data.empty:
#         return render(request, "prediction.html", {"error": "No candidates meet the criteria."})

#     # Normalize features
#     scaler = MinMaxScaler()
#     data[['attendance_score', 'backlog_score', 'policy_score']] = scaler.fit_transform(
#         data[['attendance_score', 'backlog_score', 'policy_score']]
#     )
#     data['final_score'] = (
#         0.4 * data['attendance_score'] + 0.3 * data['backlog_score'] + 0.3 * data['policy_score']
#     )

#     # Identify the best candidate for each position
#     best_candidates = data.loc[data.groupby('position')['final_score'].idxmax()]

#     # Add explanation for each selected candidate
#     best_candidates['reason'] = best_candidates.apply(
#         lambda row: f"Selected for {row['position']} due to high attendance ({row['attendance']}%), "
#                     f"minimal backlogs ({row['backlog']}), and strong policies."
#                     if row['policy_score'] > 0 else
#                     f"Selected for {row['position']} due to high attendance ({row['attendance']}%) and minimal backlogs ({row['backlog']}), "
#                     f"despite weaker policies.",
#         axis=1
#     )

#     # Convert results for rendering
#     results = best_candidates[['name', 'position', 'policy1', 'policy2', 'policy3', 
#                                 'attendance', 'backlog', 'final_score', 'reason']].to_dict(orient='records')

#     return render(request, "prediction.html", {"results": results})

from .models import candidate, nomination
from sklearn.ensemble import RandomForestClassifier
from sentence_transformers import SentenceTransformer
import pandas as pd

def predict_best_candidate(request):
    # Load data from models and only consider matching name and position
    candidates = pd.DataFrame(candidate.objects.all().values())
    nominations = pd.DataFrame(nomination.objects.all().values())

    # Merge data on relevant fields (name and position)
    data = pd.merge(candidates, nominations, on=['name', 'position'], how='inner')

    # If no matching data found, return an error
    if data.empty:
        return render(request, "prediction.html", {"error": "No matching data found for candidates and nominations"})

    # Process attendance as percentage (higher attendance = better)
    data['attendance_score'] = data['attendance'].astype(float)

    # NLP embeddings for policy evaluation (using Sentence Transformer for policy evaluation)
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    data['policy_score'] = data.apply(
        lambda row: model.encode(row['policy1'] + " " + row['policy2'] + " " + row['policy3']).mean(),
        axis=1
    )

    # Process backlog (lower backlogs = better, prioritize 0 backlogs)
    data['backlog_score'] = data['backlog'].apply(lambda x: 0 if x.lower() == 'none' else int(x))

    # Initialize an empty list to store best candidates for each position
    best_candidates = []

    # Loop through each unique position and select the best candidate
    for position in data['position'].unique():
        position_data = data[data['position'] == position]
        
        # Filter to prioritize candidates with 0 backlogs (best)
        position_best_candidates = position_data[position_data['backlog_score'] == 0]

        # If no candidates with 0 backlogs, prioritize candidates with 1 backlog, then 2, etc.
        if position_best_candidates.empty:
            position_best_candidates = position_data[position_data['backlog_score'] == 1]
        if position_best_candidates.empty:
            position_best_candidates = position_data[position_data['backlog_score'] == 2]

        # Calculate overall score based on attendance and policy (higher scores are better)
        position_best_candidates['candidate_score'] = position_best_candidates['attendance_score'] + position_best_candidates['policy_score']

        # Select the best candidate for the position based on the highest score
        best_for_position = position_best_candidates.loc[position_best_candidates.groupby('position')['candidate_score'].idxmax()]

        # Append the selected candidate to the list
        best_candidates.append(best_for_position)

    # Concatenate the best candidates for each position into a single dataframe
    best_candidates_df = pd.concat(best_candidates)

    # Prepare results for rendering
    results = best_candidates_df[['name', 'position', 'policy1', 'policy2', 'policy3', 'attendance', 'backlog', 'candidate_score']]
    
    # Add a reason for selecting the candidate
    results['reason'] = results.apply(lambda row: f"Highest attendance: {row['attendance']}, Fewest backlogs: {row['backlog']}, Best policies.", axis=1)

    # Render the results in the template
    return render(request, "prediction.html", {"results": results.to_dict(orient='records')})


from django.shortcuts import render,get_object_or_404
from .models import PostModel
def createPost(request):
    candidateid = request.session.get('candidateid')
    if candidateid:
        user_dtls = get_object_or_404(candidate, candidateid=candidateid)
        if request.method == "POST":
            post_pic = request.FILES.get('post_pic')
            description = request.POST.get('description')
            like_count = 0

            PostModel(
                user=user_dtls,
                post_pic=post_pic,
                description=description,
                likes_count=like_count,
            ).save()
            return redirect('cdisplay_posts')
        return render(request, 'addpost.html')
    return redirect('home')

def displayPosts(request):
    posts = PostModel.objects.all()
    post_comments = {}

    for post in posts:
        if post.post_pic:
            post.is_video = post.post_pic.url.endswith(('.mp4', '.webm', '.ogg'))
            post.is_pdf = post.post_pic.url.endswith('.pdf')
            post.is_image = not (post.is_video or post.is_pdf)
        else:
            post.is_video = post.is_pdf = post.is_image = False

    return render(request, 'display_posts.html', {'posts': posts})

def fdisplayPosts(request):
    posts = PostModel.objects.all()
    post_comments = {}

    for post in posts:
        if post.post_pic:
            post.is_video = post.post_pic.url.endswith(('.mp4', '.webm', '.ogg'))
            post.is_pdf = post.post_pic.url.endswith('.pdf')
            post.is_image = not (post.is_video or post.is_pdf)
        else:
            post.is_video = post.is_pdf = post.is_image = False

    return render(request, 'fdisplay_posts.html', {'posts': posts})
def cdisplay_Posts(request):
    posts = PostModel.objects.all()
    post_comments = {}

    for post in posts:
        if post.post_pic:
            post.is_video = post.post_pic.url.endswith(('.mp4', '.webm', '.ogg'))
            post.is_pdf = post.post_pic.url.endswith('.pdf')
            post.is_image = not (post.is_video or post.is_pdf)
        else:
            post.is_video = post.is_pdf = post.is_image = False

    return render(request, 'cdisplay_posts.html', {'posts': posts})
def sdisplay_Posts(request):
    posts = PostModel.objects.all()
    post_comments = {}

    for post in posts:
        if post.post_pic:
            post.is_video = post.post_pic.url.endswith(('.mp4', '.webm', '.ogg'))
            post.is_pdf = post.post_pic.url.endswith('.pdf')
            post.is_image = not (post.is_video or post.is_pdf)
        else:
            post.is_video = post.is_pdf = post.is_image = False

    return render(request, 'sdisplay_posts.html', {'posts': posts})
def viewpost(request):
    email = request.session.get('candidateid')
    if email:
        posts = PostModel.objects.filter(user__email=email)
        for post in posts:
            if post.post_pic:
                file_extension = post.post_pic.url.lower().split('.')[-1]
                if file_extension in ['jpg', 'jpeg', 'png']:
                    post.file_type = 'image'
                elif file_extension in ['mp4', 'mov']:
                    post.file_type = 'video'
                elif file_extension == 'pdf':
                    post.file_type = 'pdf'
                else:
                    post.file_type = 'other'
            else:
                post.file_type = 'other'
        return render(request, 'viewpost.html', {'post': posts})
    return redirect('viewpost')

def deletepost(request, id):
    post = PostModel.objects.get(id=id)
    post.delete()
    return redirect('viewpost')  



def editepost(request, id):
    post = PostModel.objects.get(id=id)
    if request.method == 'POST':
        description = request.POST.get('description')
        post_pic = request.FILES.get('image')
        post.description = description
        if post_pic:
            post.post_pic = post_pic
        post.save()
        return redirect('viewpost')
    return render(request, 'editpost.html', {'edit': post})

def get_notifications(request):
    notifications = notification.objects.order_by('-created_at')[:10]
    data = [{"message": n.message, "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S")} for n in notifications]
    return JsonResponse(data, safe=False)

