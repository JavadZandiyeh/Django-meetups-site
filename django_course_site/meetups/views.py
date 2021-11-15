from django.shortcuts import redirect, render
from .models import Meetup, Participation
from .forms import RegistrationForm

# Create your views here.
def index(request):
    meetups_list = Meetup.objects.all()
    return render(request, 'meetups/index.html', {
        'show_meetups': True,
        'meetups_list': meetups_list
    })

def meetup_details(request, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if request.method == "GET":
            registration_form = RegistrationForm()
        else: # for POST request
            registration_form = RegistrationForm(request.POST)
            # check validation and store in database
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant, was_created = Participation.objects.get_or_create(email=user_email)
                selected_meetup.participation.add(participant)
                return redirect('confirm-registration', meetup_slug=meetup_slug)

        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': True,
            'meetup': selected_meetup,
            'registration_form': registration_form, 
        })
    except Exception as exc:
        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': False
        })

def confirm_registration(request, meetup_slug):
    selected_meetup = Meetup.objects.get(slug=meetup_slug)
    return render(request, 'meetups/registration-success.html', {
        'organizer_email': selected_meetup.organizer_email
    })
