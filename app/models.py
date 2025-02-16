from django.db import models
from django.utils import timezone
# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=50)
    phoneno=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=50,blank=True)
    registerno=models.CharField(max_length=10)
    course=models.CharField(max_length=50)
    department=models.CharField(max_length=50)

class faculty(models.Model):
      facultyid=models.CharField(max_length=20)
      password=models.CharField(max_length=50)
      name=models.CharField(max_length=50)
      department=models.CharField(max_length=10)
      phoneno=models.IntegerField()
      email=models.EmailField(max_length=100)

class candidate(models.Model):
     candidateid=models.CharField(max_length=50)
     password=models.CharField(max_length=50,blank=True)
     name=models.CharField(max_length=50)
     department=models.CharField(max_length=50)
     course=models.CharField(max_length=50)
     position=models.CharField(max_length=50,null=True,blank=True)
     policy1=models.CharField(max_length=100)
     policy2=models.CharField(max_length=100)
     policy3=models.CharField(max_length=100)
     avatar=models.ImageField(upload_to="photo/" ,null=True,blank=True)
     def __str__(self):
        return f"{self.name} {self.position}"
     

class nomination(models.Model):
    studentid = models.ForeignKey(student, on_delete=models.CASCADE)
    tutor_in_charge = models.ForeignKey(faculty, on_delete=models.CASCADE, related_name="nominations") 
    name=models.CharField(max_length=30)
    phoneno=models.IntegerField()
    email=models.EmailField(max_length=100)
    regno=models.CharField(max_length=10,unique=True)
    department=models.CharField(max_length=30)
    course=models.CharField(max_length=30)
    year=models.CharField(max_length=20)
    attendance=models.CharField(max_length=20)
    backlog=models.CharField(max_length=20)
    position=models.CharField(max_length=20)
    status=models.CharField(max_length=20) 
    created_at=models.DateTimeField(default=timezone.now)
#chatsection

 
#chatsection
class Room(models.Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{str(self.room)} - {self.sender}"
    

class Vote(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE)  # Link to the User who is voting
    chairperson = models.ForeignKey(candidate, null=True, blank=True, related_name="chairperson_votes", on_delete=models.SET_NULL)
    vice_chairperson = models.ForeignKey(candidate, null=True, blank=True, related_name="vice_chairperson_votes", on_delete=models.SET_NULL)
    general_secretary = models.ForeignKey(candidate, null=True, blank=True, related_name="general_secretary_votes", on_delete=models.SET_NULL)
    joint_secretary = models.ForeignKey(candidate, null=True, blank=True, related_name="joint_secretary_votes", on_delete=models.SET_NULL)
    fine_arts_secretary = models.ForeignKey(candidate, null=True, blank=True, related_name="fine_arts_secretary_votes", on_delete=models.SET_NULL)
    student_editor = models.ForeignKey(candidate, null=True, blank=True, related_name="student_editor_votes", on_delete=models.SET_NULL)
    uuc_rep_1 = models.ForeignKey(candidate, null=True, blank=True, related_name="uuc_rep_1_votes", on_delete=models.SET_NULL)
    uuc_rep_2 = models.ForeignKey(candidate, null=True, blank=True, related_name="uuc_rep_2_votes", on_delete=models.SET_NULL)

    # Add additional fields for other positions as necessary

    submitted_at = models.DateTimeField(auto_now_add=True)  # Time when the vote was cast

    def __str__(self):
        return f"Vote by {self.user.name} on {self.submitted_at}"

class notification(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    
class PostModel(models.Model):
    user = models.ForeignKey(candidate, on_delete=models.CASCADE, related_name='posts')
    post_pic = models.ImageField(upload_to='posts/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(candidate, related_name='liked_posts', blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.name} - {self.description[:20]}"

class Admin(models.Model):
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=50,blank=True)
