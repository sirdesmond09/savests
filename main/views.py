from django.shortcuts import render, redirect
from .models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

@staff_member_required
def deactivate_user(request, id):
    

    user = User.objects.get(id=id)
    if user.is_active == True:
        user.is_active = False
        user.save()

        return redirect('admin/main/user/')
    else:
        user.is_active=True
        user.save()

        return redirect('admin/main/user/')

    


@staff_member_required
def mail_user(request):

    if request.method == 'POST':
        print(request.user)
        # admin = request.user
        recipient_list = []

        #we get all the users except the superusers
        user = User.objects.filter(is_superuser=False)

        #we get all the user's email
        for i in user:
            recipient_list.append(i.email)

        subject = request.POST['subject']
        from_mail = request.POST['sender']
        print(recipient_list)
        print(from_mail)

        message = request.POST['message']
        
        
        send_mail(subject, message, from_mail , recipient_list)
        messages.success(request, "Your message has been sent successfully!")
        
        return render(request, 'admin/mail.html', )
    
    context = {
        
    }
    return render(request,'admin/mail.html',context)