from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout,get_user_model
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, DocumentForm,EmergencyContactForm,DocumentImageFormSet,DocumentImage,UpdateUserForm,ProfilePictureForm
from .models import Document,Profile,EmergencyContact,Feedback
from django.core.mail import send_mail

# Create your views here.
def Home(request):
    return render(request,'home.html',locals())

def profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
    return render(request,'profile.html',locals())

def profile_details(request,pk):
    if request.user.is_authenticated:
        profile_details = Profile.objects.get(user_id=pk)
    return render(request,'profile_details.html',locals())

def document(request):
    documents = Document.objects.filter(user=request.user)
    return render(request,'documents.html',locals())

def document_view(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    return render(request, 'document_view.html', {'document': document})

def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('documents')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_edit.html', locals())

def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        document.delete()
        messages.success(request, f'Your Document as been deleted successfully')
        return redirect('documents')
    return render(request, 'document_confirm_delete.html', {'document': document})

def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        formset = DocumentImageFormSet(request.POST, request.FILES, queryset=DocumentImage.objects.none())

        if form.is_valid() and formset.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    DocumentImage.objects.create(document=document, image=image)

            return redirect('documents')  # Replace with your success URL
    else:
        form = DocumentForm()
        formset = DocumentImageFormSet(queryset=DocumentImage.objects.none())
    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         document = form.save(commit=False)
    #         document.user = request.user
    #         document.save()
    #         return redirect('documents')
    # else:
    #     form = DocumentForm()
    return render(request,'document_create.html',locals())

def profile_info(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # user_form = SignUpForm(request.POST, instance=user)
        profile_form = UpdateUserForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            messages.success(request,'Your profile have been updated!!!!')
            return redirect('profile_info')
    else:
        user_form = SignUpForm(instance=user)
        profile_form = UpdateUserForm(instance=profile)
    # if request.user.is_authenticated:
    #     current_user = User.objects.get(id=request.user.id)
    #     profile_user = Profile.objects.get(user__id=request.user.id)

    #     user_form = SignUpForm(request.POST or None, request.FILES or None,instance=current_user)
    #     profile_form = UpdateUserForm(request.POST or None, request.FILES or None,instance=profile_user)
    #     if user_form.is_valid() and profile_form.is_valid():
    #       user_form.save()  
    #       profile_form.save()
    #       login(request,current_user)
    return render(request,'profile_info.html',locals())

@login_required
def emergency_contact_list(request):
    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request, 'emergency_contact.html', locals())
@login_required
def emergency_contact_add(request):
    if EmergencyContact.objects.filter(user=request.user).count() >= 4:
        messages.warning(request, 'You can only add up to 4 emergency contacts.')
        return redirect('emergency-contact-list')

    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Emergency contact added successfully!')
            return redirect('emergency-contact-list')
    else:
        form = EmergencyContactForm()
    return render(request, 'emergency_contact.html', locals())

@login_required
def emergency_contact_edit(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emergency contact updated successfully!')
            return redirect('emergency-contact-list')
    else:
        form = EmergencyContactForm(instance=contact)
    return render(request, 'emergency_contact.html', locals())

@login_required
def emergency_contact_delete(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Emergency contact deleted successfully!')
        return redirect('emergency-contact-list')
    return render(request, 'emergency_contact.html', locals())

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,f'Welcome {request.user.username}')
                return redirect('home')
        else:
            messages.success(request,'Invalid username or password')
            return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request,'login.html',locals())
    
def logout_user(request):
    user = request.user
    user.profile.is_active = False 
    user.delete() 
    logout(request)
    messages.info(request,'You have been log out')
    return redirect('login')

def Register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            #email verification
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request,'please check your email to complete your registration')
            return redirect('home')

            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # # you can also clean rest of the info if you needed but it not required
            # user = authenticate(username=username, password=password)
            # login(request,user)
            # messages.success(request,'You have successfully log in')
            # return redirect('home')
        

    return render(request,'register.html',locals())

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user) 
        messages.success(request,'Your account have been activated..You can now login')
        return redirect(reverse('login'))
    else:
        messages.error(request,'Activattion link is invalid or expired..')
        return redirect('login')

def Contact(request):
    return render(request,'contact.html',locals())

def About(request):
    return render(request,'about.html',locals())

def settings(request):
    return render(request,'settings.html',locals())

def deactivate_account(request):
    user = request.user
    user.profile.is_active = False  
    user.profile.save()
    logout(request)  
    return redirect('home') 

@login_required
def delete_account(request):
    user = request.user
    logout(request)  # Log the user out before deleting
    user.delete()  # This will also trigger the signal to delete related data
    return redirect('home') 

def profile_picture_change(request):
    if request.method == 'POST':
        p_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile picture have been change successfully!!')
            return redirect('profile_info')  # Redirect to the user's profile page after updating
    else:
        p_form = ProfilePictureForm(instance=request.user.profile)

   
    return render(request,'profilepics.html',locals())

def write_feedback(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            # Save feedback to the database
            Feedback.objects.create(user=request.user, content=content)

            # Send email notification
            send_mail(
                subject=f"New Feedback from {request.user.username}",
                message=f"Feedback content:\n\n{content}\n\nUser email: {request.user.email}",
                from_email="noreply@mylife.com",
                recipient_list=["adeshinasmart@gmail.com"],  # Replace with your admin/support email
            )
            send_mail(
                subject="Thank you for your feedback!",
                message="Hi {0},\n\nThank you for taking the time to share your thoughts with us. We value your input and will review it shortly.\n\nBest regards,\nThe MyLife Team".format(request.user.username),
                from_email="noreply@mylife.com",
                recipient_list=[request.user.email],
                )

            messages.success(request, "Thank you for your feedback!")
            return redirect("home")
        else:
            messages.error(request, "Feedback content cannot be empty.")
    return render(request,'write_feedback.html',locals())

@login_required
def feedback_history(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")  # Latest feedback first
    return render(request, "feedback_history.html", {"feedbacks": feedbacks})


@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    # Ensure only the owner can delete their feedback
    if feedback.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this feedback.")

    if request.method == "POST":
        feedback.delete()
        messages.success(request, "Feedback deleted successfully!")
        return redirect("feedback_history")

    return render(request, "confirm_delete.html", {"feedback": feedback})
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)  # Optionally log the user in immediately after activation
#         return render(request, 'registration/activation_success.html')  # Redirect to success page
#     else:
#         return render(request, 'registration/activation_invalid.html')