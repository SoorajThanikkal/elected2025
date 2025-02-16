from django.contrib import admin
from . models import student,faculty,candidate,nomination,notification,PostModel,Admin
admin.site.register(candidate)

admin.site.register(faculty)
# Register your models here.
admin.site.register(student)
admin.site.register(nomination)
admin.site.register(notification)
admin.site.register(PostModel)


from .models import Room, Message,Vote


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Vote)
admin.site.register(Admin)
