# Django
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

# Functions-based views
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Class-based views
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Account
from django.contrib.auth import logout, get_user_model

# Email confirmation
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import account_activation_token

# Password reset
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import reverse_lazy

# Booking
from django.http import JsonResponse
from datetime import timedelta, datetime, time

# Pro Area
from django.contrib import messages

# Payment
from django.conf import settings
import stripe
import time

# Import
from .models import CustomGroup, Event, Concert, CustomUser, Reservation, Salle, UserPayment 
from .forms import (
    UserSignInForm, UserSignUpForm, UserSignUpAgainForm,
    ProfileUpdateForm, ProfileUpdateConfirmForm,
    PasswordForgotResetForm, PasswordForgotSetForm,
    CustomGroupForm,
    ConcertForm,
    EventForm, ReservationForm)

User = get_user_model()



# Create your views here.
"""
Placeholder
"""
def placeholder(request):
    return render(request, 'home.html')


"""
Navigation
    - HomeView
    - NewsView
    - StudiosView
    - ConcertView
    - BarView
    - BookingView
    - ContactView
"""
class HomeView(View):
    template_name = "home.html"
    context = {
        "title": "Covent Garden"
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class NewsView(View):
    template_name = "news.html"
    context = {
        "title": "Actualités",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Actualités"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class StudiosView(View):
    template_name = "studios.html"
    context = {
        "title": "Studios",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Studios"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class ConcertView(View):
    template_name = "concert.html"
    context = {
        "title": "Concert",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Concert"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)
    


class BarView(View):
    template_name = "bar.html"
    context = {
        "title": "Bar",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Bar"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class BookingView(View):
    template_name = "booking.html"
    context = {
        "title": "Réservation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Réservation"}]
    }

    def get(self, request):
        self.context["salles"] = Salle.objects.all()
        return render(request, self.template_name, self.context)


class ContactView(View):
    template_name = "contact.html"
    context = {
        "title": "Contact",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Contact"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)



class EulaView(View):
    template_name = "cgu.html"
    context = {
        "title": "Conditions générales d'utilisation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Conditions générales d'utilisation"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)




"""
Account
    - AccountSignInFormView
    - AccountSignUpFormView
    - AccountSignUpDoneView
    - AccountSignUpCompleteView
    - AccountSignUpFailedView
    - AccountPasswordForgotForm
    - AccountPasswordForgotDone
    - AccountPasswordForgotConfirm
    - AccountPasswordForgotComplete
    - account_log_out
    
WIP
    - AccountSignInFormView: Add a "User not found" error message
    - AccountSignUpFormView: Add a "Password verification failed" error message
    - account_sign_up_email: Update the email template
    - AccountPasswordForgotConfirm:
        - Find out how to modify the "Password reset unsuccessful" view
        - Find the source code for PasswordResetConfirmView
"""

class AccountSignInFormView(View):
    form_class = UserSignInForm
    template_name = "account/account_sign_in_form.html"
    context = {
        "title": "Se connecter à son compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": None, "name": "Connexion"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.login(request)
            return redirect('profile_detail')

        # Failure
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class AccountSignUpFormView(View):
    form_class = UserSignUpForm
    template_name = "account/account_sign_up_form.html"
    context = {
        "title": "Créer un compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": None, "name": "Inscription"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save_user(request)
            return redirect("account_sign_up_done")

        # Failure
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class AccountSignUpDoneView(View):
    template_name = "account/account_sign_up_done.html"
    context = {
        "title": "Envoi du mail de confirmation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "account_sign_up_form", "name": "Inscription"},
            {"view": None, "name": "Envoi"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, self.context)


class AccountSignUpConfirmView(View):
    template_name = "account/account_sign_up_confirm.html"
    context = {
        "title": "Confirmation de la création du compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "account_sign_up_form", "name": "Inscription"},
            {"view": None, "name": "Envoi"},
            {"view": None, "name": "Confirmation"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)

    def get(self, request, uidb64, token):
        # Create user
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        # Check for error
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Check for user and token
        if user is not None and account_activation_token.check_token(user, token):
            # Activate the new user
            user.is_active = True
            user.save()

            return render(request, self.template_name, self.context)

        # Failure
        return redirect("account_sign_up_failed")


class AccountSignUpFailedView(View):
    template_name = "account/account_sign_up_failed.html"
    context = {
        "title": "Échec de la création du compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "account_sign_up_form", "name": "Inscription"},
            {"view": None, "name": "Envoi"},
            {"view": None, "name": "Échec"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, self.context)


class AccountSignUpAgainView(View):
    form_class = UserSignUpAgainForm
    template_name = "account/account_sign_up_email_again.html"
    context = {
        "title": "Mail de confirmation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "account_sign_up_form", "name": "Inscription"},
            {"view": None, "name": "Vérification"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.send_email(request)
            return redirect("account_sign_up_done")

        # Failure
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class AccountPasswordForgotForm(PasswordResetView):
    form_class = PasswordForgotResetForm
    template_name = 'account/account_password_forgot_form.html'
    email_template_name = 'account/account_password_forgot_email.html'
    subject_template_name = 'account/account_password_forgot_email_subject.txt'
    success_url = reverse_lazy('account_password_forgot_done')
    extra_context = {
        "title": "Récupérer son compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": None, "name": "Mot de passe oublié"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)


class AccountPasswordForgotDone(PasswordResetDoneView):
    template_name = 'account/account_password_forgot_done.html'
    extra_context = {
        "title": "Validation de la demande",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": "account_password_forgot_form", "name": "Mot de passe oublié"},
            {"view": None, "name": "Envoi"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)


class AccountPasswordForgotConfirm(PasswordResetConfirmView):
    form_class = PasswordForgotSetForm
    template_name = 'account/account_password_forgot_confirm.html'
    success_url = reverse_lazy('account_password_forgot_complete')
    extra_context = {
        "title": "Modifier mon mot de passe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": "account_password_forgot_form", "name": "Mot de passe oublié"},
            {"view": None, "name": "Envoi"},
            {"view": None, "name": "Modifier"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)


class AccountPasswordForgotComplete(PasswordResetCompleteView):
    template_name = 'account/account_password_forgot_complete.html'
    extra_context = {
        "title": "Confirmation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": "account_password_forgot_form", "name": "Mot de passe oublié"},
            {"view": None, "name": "Envoi"},
            {"view": None, "name": "Modifier"},
            {"view": None, "name": "Confirmation"}]
    }

    def dispatch(self, *args, **kwargs):
        # Redirect if user is already authenticated
        if self.request.user.is_authenticated:
            return redirect('profile_detail')
        return super().dispatch(*args, **kwargs)


def account_log_out(request):
    logout(request)
    return redirect('account_sign_in_form')





"""
Profile
    - ProfileDetailView
    - ProfileUpdateView
"""
class ProfileDetailView(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "profile/profile_detail.html"
    context = {
        "title": "Mon compte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Compte"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class ProfileUpdateView(LoginRequiredMixin, View):
    redirect_field_name = ''
    form_class = ProfileUpdateForm
    form_confirm_class = ProfileUpdateConfirmForm
    template_name = "profile/profile_update.html"
    context = {
        "title": "Modifier mon profil",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "profile_detail", "name": "Compte"},
            {"view": None, "name": "Modifier"}],
    }

    def get(self, request):
        self.context["form"] = self.form_class(user=request.user, instance=request.user)
        self.context["form_confirm"] = self.form_confirm_class(user=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST, instance=request.user)
        form_confirm = self.form_confirm_class(user=request.user, data=request.POST)

        if form.is_valid() and form_confirm.is_valid():
            form.save()
            return redirect('profile_detail')

        # Failure
        self.context["form"] = form
        self.context["form_confirm"] = form_confirm
        return render(request, self.template_name, self.context)





"""
Groups
    - GroupDetailView
    - GroupCreateView
    - GroupUpdateView
    - GroupDeleteView
"""

class GroupDetailView(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "groups/groups_detail.html"
    context = {
        "title": "Mes groupes",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Groupes"}]
    }

    def get(self, request):
        self.context["my_groups"] = request.user.my_groups.all()

        return render(request, self.template_name, self.context)

    def post(self, request):
        return render(request, self.template_name, self.context)


class GroupCreateView(LoginRequiredMixin, View):
    redirect_field_name = ''
    form_class = CustomGroupForm
    template_name = "groups/groups_create.html"
    context = {
        "title": "Créer un groupe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "groups_detail", "name": "Groupes"},
            {"view": None, "name": "Créer"}]
    }

    def get(self, request):
        initial = {
            "name": self.request.user.username,
            "email": self.request.user.email,
            "phone": self.request.user.phone
        }
        self.context["form"] = self.form_class(initial=initial)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save_group(request)
            return redirect('groups_detail')

        # Failure
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class GroupUpdateView(LoginRequiredMixin, View):
    redirect_field_name = ''
    form_class = CustomGroupForm
    template_name = "groups/groups_update.html"
    context = {
        "title": "Modifier un groupe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "groups_detail", "name": "Groupes"},
            {"view": None, "name": "Modifier"}]
    }

    def get(self, request, group_id):
        group = CustomGroup.objects.get(id=group_id)
        self.context["form"] = self.form_class(instance=group)
        return render(request, self.template_name, self.context)

    def post(self, request, group_id):
        group = CustomGroup.objects.get(id=group_id)
        form = self.form_class(request.POST, request.FILES, instance=group)

        if form.is_valid():
            form.save_group(request)
            return redirect('groups_detail')

        # Failure
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)

class GroupDeleteView(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "groups/groups_delete.html"
    context = {
        "title": "Supprimer un groupe",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "groups_detail", "name": "Groupes"},
            {"view": None, "name": "Supprimer"}]
    }

    def get(self, request, group_id):
        return render(request, self.template_name, self.context)

    def post(self, request, group_id):
        # Redirect to login page if user is not logged in
        if not request.user.is_authenticated:
            return redirect("account_sign_in_form")

        CustomGroup.objects.get(id=group_id).delete()
        return redirect('groups_detail')












"""
Bookings
    - BookingsDetailView
    - BookingsCreateView
"""
class BookingsDetailView(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "bookings/bookings_detail.html"
    context = {
        "title": "Historique des réservations",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Réservations"}]
    }

    def get(self, request):
        # Get all groups object related to the current user
        self.context["my_groups"] = request.user.my_groups.all()

        # Get all reservations for user
        reservations = Reservation.objects.filter(user_id=request.user.id, is_active=True)
        self.context["reservations"] = reservations

        return render(request, self.template_name, self.context)


class BookingsCreateView(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "bookings/bookings_create.html"
    context = {
        "title": "Créer une réservation",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "bookings_detail", "name": "Réservations"},
            {"view": None, "name": "Créer"}]
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


"""
Pro area
    - ProAreaView
"""
class ProAreaView(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "pro_area.html"
    context = {
        "title": "Espace Pro",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": None, "name": "Espace Pro"}]
    }

    def get(self, request):
        self.context["form"] = ConcertForm()
        return render(request, self.template_name, self.context)

    def post(self, request):
        self.context["form"] = ConcertForm(request.POST)
        if self.context["form"].is_valid():
            self.context["form"].save()
            messages.success(request,
                             'Merci pour votre proposition de concert! Un administrateur examinera votre proposition prochainement.',
                             extra_tags='concert_for')
        
        return render(request, self.template_name, self.context)


"""
Planning
"""
def generate_occurrences(event):
    occurrences = [event.start_time]

    if event.recurrence == 'daily':
        current_time = event.start_time
        while current_time < event.end_time:
            current_time += timedelta(days=1)
            occurrences.append(current_time)

    return occurrences



def add_event(request):
    # Submit form
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


def index(request):
    all_events = Event.objects.all()

    events = []
    for event in all_events:
        occurrences = generate_occurrences(event)
        for occurrence in occurrences:
            events.append({
                'title': event.title,
                'id': event.id,
                'start': occurrence.strftime("%Y-%m-%d %H:%M:%S"),
                'end': occurrence.strftime("%Y-%m-%d %H:%M:%S"),
            })

    context = {
        "events": events,
    }
    return render(request, 'index.html', context)


def all_events(request):
    events = Event.objects.all()
    out = []
    for event in events:
        out.append({
            'title': event.title,
            'id': event.id,
            'start': event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse(out, safe=False)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.start_time = start
    event.end_time = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


def calendar_view(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'calendar.html', context)


"""
Salles
    -Listing all Salle
Reservation
    - Listing reservation
"""
def is_in_group(CustomUser):
    return CustomUser.groups.filter(name='CLIENT_REGULIER').exists()


def list_salles(request):
    salles = Salle.objects.all()
    salle_data = [{"id": salle.id, "title": salle.name} for salle in salles]
    return JsonResponse(salle_data, safe=False)

def list_users(request):
    users = CustomUser.objects.all()
    user_data = [{"id": user.id, "title": user.username} for user in users]
    return JsonResponse(user_data, safe=False)

@login_required(login_url='account_sign_in_form')
def accompte(request):
    # Submit form
    if request.method == 'POST':

        salle_id = int(request.POST["salle_id"])
        salle = Salle.objects.get(id= salle_id)

        user_id = int(request.POST["user_id"])
        user = CustomUser.objects.get(id= user_id)

        start_date = request.POST["date_start"]
        end_date = request.POST["date_end"]
        
        form = ReservationForm()

        duration = datetime.fromisoformat(end_date.rstrip('Z')) - datetime.fromisoformat(start_date.rstrip('Z'))
        duration_seconds = duration.total_seconds()
        duration_hours = duration_seconds / 3600

        if duration_hours == 1. : 
            price = 10.0
        elif duration_hours == 2. : 
            price = 19.0
        elif duration_hours == 3. : 
            price = 27.0
        elif duration_hours == 4. : 
            price = 34.0
        elif duration_hours == 5. : 
            price = 42.0 
        elif duration_hours == 6. : 
            price = 51.0
        elif duration_hours == 7. : 
            price = 59.0
        else: 
            price = 68.0        
        start_date = datetime.fromisoformat(start_date.rstrip('Z'))
        end_date = datetime.fromisoformat(end_date.rstrip('Z'))
        #duration = 1

        if is_in_group(user):
            description = "Reservation for user "+ user.username
            status = "En cours"
            reservation = Reservation.objects.create(
                description=description,
                duration=duration_hours,
                date_start=start_date,
                date_end=end_date,
                price=0,
                status=status,
                salle=salle,
                user=user,
                is_active=True
            )
            messages.success(request, "Votre réservation a bien été prise en compte !")
            return redirect('booking')

        else:
            return render(request, 'payment.html', {"salle": salle, "user": user, "start_date": start_date,
            "end_date": end_date, "duration": duration_hours,"price":price, "form": form})

    else:
        return redirect('booking')
    

@login_required(login_url='account_sign_in_form')
def payment_without_stripe(request):

    print(request.POST)

    # Submit form
    if request.method == 'POST':

        salle_id = int(request.POST["salle_id"])
        user_id = int(request.POST["user_id"])

        form = ReservationForm(request.POST)

        if form.is_valid():

            salle = Salle.objects.get(id= salle_id)
            user = CustomUser.objects.get(id= user_id)

            description = "Reservation for user "+ user.username
            duration = form.cleaned_data["duration"]
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            price = form.cleaned_data["price"]
            status = "En cours"

            reservation = Reservation.objects.create(
                description=description,
                duration=duration,
                date_start=date_start,
                date_end=date_end,
                price=price,
                status=status,
                salle=salle,
                user=user,
                is_active=True
            )

            messages.success(request, "Votre réservation a bien été prise en compte !")
            return redirect('booking')

    else:
        return redirect('booking')

def all_booking(request):
    reservations = Reservation.objects.all()
    datas = []
    for current in reservations:
        datas.append({
            'title': current.description,
            'id': current.id,
            'start': current.date_start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': current.date_end.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse(datas, safe=False)

def all_booking_event(request):
    reservations = Reservation.objects.all()
    datas = []
    datas.append({'firstDay': 1})

    for current in reservations:
        # Vérifier si le jour de la réservation est du lundi au vendredi
        if current.date_start.weekday() < 5:
            data = {
                'id': current.id,
                'resourceId': current.salle.id,
                'title': 'Indisponible',
                'start': current.date_start,
                'end': current.date_end,
                'color': '#b22222',
                'textColor': 'black'
            }
            datas.append(data)

    dataD = []
    dateInit = datetime(2023, 1, 2)

    for resource in Salle.objects.all():
        for i in range(365):
            # Vérifier si le jour est du lundi au vendredi
            if (dateInit + timedelta(days=i)).weekday() < 5:
                
                new_data = {
                    'id': 1,  # Modifier ici
                    'resourceId': resource.id,
                    'title': 'Indisponible',
                    'start': (dateInit + timedelta(days=i)).replace(hour=10, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'end': (dateInit + timedelta(days=i)).replace(hour=16, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'color': 'gainsboro',
                    'textColor': 'black'
                }
                datas.append(new_data)
                new_data['id'] += 1  # Modifier ici
            if (dateInit + timedelta(days=i)).weekday() == 5:
                new_data = {
                    'id': 1,
                    'resourceId': resource.id,
                    'title': 'Indisponible',
                    'start': (dateInit + timedelta(days=i)).replace(hour=18, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'end': (dateInit + timedelta(days=i)).replace(hour=23, minute=59, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'color': 'gainsboro',
                    'textColor': 'black'
                }
                datas.append(new_data)
                new_data['id'] += 1
            if (dateInit + timedelta(days=i)).weekday() == 6:
                new_data = {
                    'id': 0,
                    'resourceId': resource.id,
                    'title': 'Indisponible',
                    'start': (dateInit + timedelta(days=i)).replace(hour=10, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'end': (dateInit + timedelta(days=i)).replace(hour=13, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'color': 'gainsboro',
                    'textColor': 'black'
                }
                datas.append(new_data)
                new_data['id'] += 1
            if (dateInit + timedelta(days=i)).weekday() == 6:
                new_data = {
                    'id': 1,
                    'resourceId': resource.id,
                    'title': 'Indisponible',
                    'start': (dateInit + timedelta(days=i)).replace(hour=21, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                    'end': (dateInit + timedelta(days=i)).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S"),
                    'color': 'gainsboro',
                    'textColor': 'black'
                }
                datas.append(new_data)
                new_data['id'] += 1
    return JsonResponse(datas, safe=False)

@login_required(login_url='account_sign_in_form')
def set_reservation(request):
    if request.method == 'POST':

        id_reservation = int(request.POST["reservation_id"])

        reservation = Reservation.objects.get(id=id_reservation)

        current_datetime = datetime.now()
        start_datetime = reservation.date_start

        if current_datetime < start_datetime - timedelta(hours=48) or reservation.date_end > current_datetime :
            if reservation.is_active == True:
                reservation.delete()
                message = "Votre réservation a bien été annuler !"
            else:
                reservation.is_active=True
                message = "Votre réservation a bien été prise en compte !"
                reservation.save()
        else:
            message = "Cette réservation ne peut plus être modifiée !"
            messages.error(request, message)  
            return redirect('bookings_detail')

        messages.success(request, message)  
        return redirect('bookings_detail')

    else:
        return redirect('home')


@login_required(login_url='account_sign_in_form')
def payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    URL = get_local_url(request)
    if request.method == 'POST':
        salle_id = int(request.POST["salle_id"])
        user_id = int(request.POST["user_id"])

        form = ReservationForm(request.POST)

        if form.is_valid():
            salle = Salle.objects.get(id=salle_id)
            user = CustomUser.objects.get(id=user_id)

            description = "Reservation for user " + user.username
            duration = form.cleaned_data["duration"]
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            price = form.cleaned_data["price"]
            status = "En cours"

        if price == 10.0 :
                settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_1H
        elif price == 19.0:
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_2H
        elif price == 27.0:
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_3H
        elif price == 34.0:
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_4H
        elif price == 42.0:        
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_5H
        elif price == 51.0:
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_6H
        elif price == 59.0:
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_7H
        else:
            settings.PRODUCT_PRICE = settings.PRODUCT_PRICE_8H

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url = URL +"/payment_successful/{CHECKOUT_SESSION_ID}",
            cancel_url = URL + "/payment_cancelled/{CHECKOUT_SESSION_ID}"
        )
        print('############## API Stripe creation de session ############################# ')
        print(f'############## SERVER IP ############################# {URL}')
        print(checkout_session)
        if checkout_session.status == 'open' :
            reservation = Reservation.objects.create(
                description=description,
                duration=duration,
                date_start=date_start,
                date_end=date_end,
                price=price,
                status=status,
                salle=salle,
                user=user,
                is_active=False,
                session_id=checkout_session.id)
            userPayment = UserPayment.objects.create(
                app_user=user,
                payment_bool=False,
                stripe_checkout_id=checkout_session.id
            )
            
            return redirect(checkout_session.url)
    
    return redirect('booking')


def payment_successful(request, session_id):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	#checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(session_id)
	customer = stripe.Customer.retrieve(session.customer)
	user_id = request.user.id
	studios = UserPayment.objects.get(app_user=user_id,stripe_checkout_id=session_id)
	studios.stripe_checkout_id = session_id
	studios.save()
	return redirect('payment_successful')


def payment_cancelled(request, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    reservation = Reservation.objects.get(session_id=session_id)
    reservation.delete()
    return redirect('payment_cancelled')

class PaiementCancelled(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "payment_cancelled.html"

    context = {
        "title": "Paiement accompte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "booking", "name": "Réservation"},
            {"view": None, "name": "Paiement accompte"}]
    }

    def get(self, request):
        message = "La transaction a été annulé ! Veuillez recommencer à nouveau l'opération"
        messages.error(request, message)
        return render(request, self.template_name, self.context)


class PaiementSuccessful(LoginRequiredMixin, View):
    redirect_field_name = ''
    template_name = "payment_successful.html"

    context = {
        "title": "Paiement accompte",
        "breadcrumb": [
            {"view": "home", "name": "Accueil"},
            {"view": "booking", "name": "Réservation"},
            {"view": None, "name": "Paiement accompte"}]
    }

    def get(self, request):
        message = "La transaction a été réalisé avec success ! Votre reservation a été prise en compte !"
        messages.success(request, message)
        return render(request, self.template_name, self.context)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event and event['type'] == 'checkout.session.completed':
        if event['data']['object']['payment_status'] == "paid" and event['data']['object']['status'] == "complete":
            session = event['data']['object']
            session_id = session.get('id', None)
            time.sleep(15)
            reservation = Reservation.objects.get(session_id=session_id)
            reservation.is_active = True
            reservation.status = "Reserver"
            reservation.save()

            studios = UserPayment.objects.get(stripe_checkout_id=session_id)
            studios.payment_bool = True
            studios.save()
    return HttpResponse(status=200)


def get_local_url(request):
    server_name = request.META.get('REMOTE_ADDR')
    server_port = request.META.get('SERVER_PORT')
    local_url = f"http://{server_name}:{server_port}"
    url = request.META.get('HTTP_ORIGIN')
    print(f'############## URL ############################# {url}')
    return url
