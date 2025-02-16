from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('reg/',views.reg,name='reg'),
    
    path('profile/',views.profile,name='profile'),
    path('studenthome/',views.studenthome,name='studenthome'),
    path('studentlogin/',views.studentlogin,name='studentlogin'),

    path('logout/',views.logout,name='logout'),
    path('editprofile/',views.editprofile,name='editprofile'),

    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),

    path('candidatelogin/',views.candidatelogin,name='candidatelogin'),
    path('candidatehome/',views.candidatehome,name='candidatehome'),
    path('candidatereg/',views.candidatereg,name='candidatereg'),
    path('candidateprofile/',views.candidateprofile,name='candidateprofile'),
    path('candidateeditprofile/',views.candidateeditprofile,name='candidateeditprofile'),

    path('facultylogin/',views.facultylogin,name='facultylogin'),
    path('facultyhome/',views.facultyhome,name='facultyhome'),
    path('facultyreg/',views.facultyreg,name='facultyreg'),
    path('facultyprofile/',views.facultyprofile,name='facultyprofile'),
    path('facultyeditprofile/',views.facultyeditprofile,name='facultyeditprofile'),
    
    path('userlist/',views.userlist,name='userlist'),
    path('candidatelist/',views.candidatelist,name='candidatelist'),
    path('facultylist/',views.facultylist,name='facultylist'),
    path('candidateview/',views.candidateview,name='candidateview'),
    path('fcandidateview/',views.fcandidateview,name='fcandidateview'),
    path('c_candidateview/',views.c_candidateview,name='c_candidateview'),

    path('changepassword/',views.changepassword,name='changepassword'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    
    path('nominationlist/',views.nominationlist,name='nominationlist'),
    path('update_nomination/<int:nomination_id>/', views.update_nomination, name='update_nomination'),
    path('sendemail/<int:nomination_id>/',views.sendemail,name='sendemail'),
    path('results/', views.election_results, name='election_results'),
    path('fresults/', views.felection_results, name='felection_results'),
    path('cresults/', views.celection_results, name='celection_results'),
    path('aresults/', views.aelection_results, name='aelection_results'),

    path('deletecandidate/<int:id>',views.deletecandidate,name='candidate'),
    path('deletefaculty/<int:id>',views.deletefaculty,name='faculty'),
    path('deleteuser/<int:id>',views.deleteuser,name='user'),
    path('deletenomination/<int:id>',views.deletenomination,name='nomination'),
    path('deletenotification/<int:id>',views.deletenotification,name='notification'),
    path('approved_nominations/',views.nominationapproved,name='approved_nominations'),

    path('nominationlist/',views.nominationlist,name='nominationlist'),
    path('notifications/',views.get_notifications,name='get_notifications'),
    path('addnotification/',views.addnotification,name='addnotification'),
    path('deletenotification/',views.viewnotification,name='deletenotification'),
    path('viewnotification/',views.viewnotification,name='viewnotification'),
   
    
    path('result/',views.result,name='result'),
   
    # path('nominationapproved/',views.nominationapproved,name='nominationapproved'),
    


    path('dupliindex2/',views.dupliindex2,name='dupliindex2'),
    path('faculty2/',views.faculty2,name='faculty2'),
    
    path('vote/',views.vote,name='vote'),
    path('vote_page/',views.vote_page,name='vote_page'),
    
    path('prediction/',views.predict_best_candidate,name='prediction'),
    
    path('create_post/',views.createPost,name='create_post'),
    path('display_posts/',views.displayPosts,name='display_posts'),
    path('fdisplay_posts/',views.fdisplayPosts,name='fdisplayposts'),
    path('cdisplay_posts/',views.cdisplay_Posts,name='cdisplay_posts'),
    path('sdisplay_posts/',views.sdisplay_Posts,name='sdisplay_posts'),
    path('viewpost/',views.viewpost,name='viewpost'),
    path('deletepost/<int:id>',views.deletepost,name='deletepost'),
    path('editepost/<int:id>/',views.editepost,name='editepost'),
    
    #chat
    # path("chat/", views.HomeView, name="chat"),
    # path("<str:room_name>/<str:username>/", views.RoomView, name="room"),
    
    
    
]
