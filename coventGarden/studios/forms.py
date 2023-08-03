# Forms
from django.forms import ModelChoiceField, ValidationError

# Authentication
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import check_password

# Email confirmation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

# Password reset
from django.contrib.auth.forms import PasswordResetForm

# Payment
from django_select2.forms import Select2Widget

# Models & Fields
from .models import CustomUser, CustomGroup, Event, Concert
from .fields import *

User = get_user_model()





# Register your forms here
"""
CustomUser
    - UserSignInForm
    - UserSignUpForm
    - UserSignUpAgainForm
"""
class UserSignInForm(forms.Form):
    """
    A form that allows users to log in to their account
    """
    error_messages = {
        'login_failed': "Le nom d'utilisateur ou le mot de passe est incorrect.",
    }
    username = FORM_USERNAME
    password = FORM_PASSWORD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """
        This function is called implicitly by default
        """
        cleaned_data = super().clean()

        # Authentication validator
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError(self.error_messages['login_failed'], code='login_failed')

        return cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)


class UserSignUpForm(forms.ModelForm):
    """
    A form allowing users to create a new account
    """
    error_messages = {
        'password_mismatch': "Les deux mots de passes ne correspondent pas.",
    }

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name', 'phone', 'password', 'password_confirm')
        widgets = {'password': forms.PasswordInput(),
                   'password_confirm': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_password_confirm(self):
        """
        This function is called implicitly according to the corresponding field
        """
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password_confirm

    def save_user(self, request):
        # Create a deactivated user
        user = CustomUser(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            phone=self.cleaned_data.get('phone'),
            is_active=False
        )
        user.set_password(self.cleaned_data.get('password'))

        # Send confirmation email
        if self.send_email(request, user):
            user.save()

    def send_email(self, request, user):
        current_site = get_current_site(request)
        subject = "Activez votre nouveau compte Covent Garden Studios"
        message = render_to_string('account/account_sign_up_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        recipient_list = [self.cleaned_data.get('email')]

        # Send mail to a local directory
        if settings.DEBUG_EMAIL:
            email = EmailMessage(subject, message, to=recipient_list)
            email.send()

        # Send mail using an email account
        elif not settings.DEBUG_EMAIL:
            with get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_ssl=settings.EMAIL_USE_SSL,
                    use_tls=settings.EMAIL_USE_TLS,
            ) as connection:
                email_from = settings.EMAIL_HOST_USER
                email = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
                email.send()

        return True


class UserSignUpAgainForm(forms.Form):
    """
    A form allowing users to send a verification email again
    """
    error_messages = {
        'email_not_found': "Aucun compte n'est associé à cette adresse e-mail.",
    }
    email = FORM_EMAIL

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError(self.error_messages['email_not_found'], code='email_not_found')
        return email

    def send_email(self, request):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        current_site = get_current_site(request)
        subject = "Activez votre nouveau compte Covent Garden Studios"
        message = render_to_string('account/account_sign_up_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        recipient_list = [self.cleaned_data.get('email')]

        # Send mail to a local directory
        if settings.DEBUG_EMAIL:
            email = EmailMessage(subject, message, to=recipient_list)
            email.send()

        # Send mail using an email account
        elif not settings.DEBUG_EMAIL:
            with get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_ssl=settings.EMAIL_USE_SSL,
                    use_tls=settings.EMAIL_USE_TLS,
            ) as connection:
                email_from = settings.EMAIL_HOST_USER
                email = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
                email.send()

        return True





"""
Profile Update
    - ProfileUpdateForm
    - ProfileUpdateConfirmForm
"""
class ProfileUpdateForm(forms.ModelForm):
    """
    A form that allows users to update their profile
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name', 'phone')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        self.user.username = self.cleaned_data.get('username')
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        self.user.email = self.cleaned_data.get('email')
        self.user.phone = self.cleaned_data.get('phone')
        if commit:
            self.user.save()
        return self.user


class ProfileUpdateConfirmForm(forms.Form):
    """
    A form that allows users to update their profile
    """
    error_messages = {
        'password_match': "Le mot de passe ne correspond pas au mot de passe défini.",
        'password_mismatch': "Les deux mots de passes ne correspondent pas.",
    }
    password = FORM_PASSWORD
    password_confirm = FORM_PASSWORD_CONFIRM

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_password(self):
        """
        This function is called implicitly according to the corresponding field
        """
        password = self.cleaned_data.get('password')
        password_user = self.user.password
        if password and password_user:
            if not check_password(password, self.user.password):
                raise ValidationError(self.error_messages['password_match'], code='password_match')
        return password

    def clean_password_confirm(self):
        """
        This function is called implicitly according to the corresponding field
        """
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password_confirm





"""
Password Forgot
    - PasswordForgotResetForm
    - PasswordForgotSetForm
"""
class PasswordForgotResetForm(PasswordResetForm):
    """
    A form that lets a user generate a link to change their password
    https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/#PasswordResetForm
    """
    email = FORM_EMAIL

class PasswordForgotSetForm(forms.Form):
    """
    A form that lets a user change their password without entering the old password
    https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/#SetPasswordForm
    """
    error_messages = {
        'password_mismatch': "Les deux mots de passes ne correspondent pas.",
    }
    password_new = FORM_PASSWORD_NEW
    password_confirm = FORM_PASSWORD_CONFIRM

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password_confirm(self):
        """
        This function is called implicitly according to the corresponding field
        """
        password_new = self.cleaned_data.get('password_new')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password_new and password_confirm:
            if password_new != password_confirm:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password_confirm

    def save(self, commit=True):
        password = self.cleaned_data["password_new"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user





"""
CustomGroup
    - CustomGroupForm
"""
class CustomGroupForm(forms.ModelForm):
    """
    A form allowing users to create a new group
    """
    class Meta:
        model = CustomGroup
        fields = '__all__'
        exclude = ('user', 'validated')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save_group(self, request):
        group = self.save(commit=False)
        group.user = request.user
        group.save()





"""
Booking
    - EventForm
"""
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'recurrence']



"""
Pro Area
    - TechnicalSheetForm
    - ConcertForm
"""
class DateInput(forms.DateInput):
    input_type = 'date'
    
    

class ConcertForm(forms.ModelForm):
    groupe1 = ModelChoiceField(queryset=CustomGroup.objects.all(), widget=Select2Widget)
    groupe2 = ModelChoiceField(queryset=CustomGroup.objects.all(), widget=Select2Widget)
    groupe3 = ModelChoiceField(queryset=CustomGroup.objects.all(), widget=Select2Widget)
    
    date = forms.DateField( widget=DateInput )    
    

    is_engaged = forms.BooleanField(
        required=True,
        label="J'accepte l'ensemble des conditions citées ci-dessus et je m'engage à ce que les 3 groupes soient disponibles et que les fiches techniques de chacun soient déposées.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Concert
        fields = ['groupe1', 'groupe2', 'groupe3', 'date', 'is_engaged']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date.weekday() != 4:
            raise ValidationError("Vous devez choisir un vendredi.")
        if Concert.objects.filter(date=date, validated=True).exists():
            raise forms.ValidationError("Ce vendredi est indisponible.")
        group1 = self.cleaned_data['groupe1']
        group2 = self.cleaned_data['groupe2']
        group3 = self.cleaned_data['groupe3']

        if group1 and (group1 == group2 or group1 == group3):
            raise forms.ValidationError("Vous ne pouvez pas choisir le même groupe plus d'une fois.")

        if group2 and group2 == group3:
            raise forms.ValidationError("Vous ne pouvez pas choisir le même groupe plus d'une fois.")

        return date

"""
Booking
"""
class ReservationForm(forms.Form):
    name = forms.CharField(max_length=LENGTH_NAME, label="Nom de l'utilisateur")
    email = forms.EmailField(label="Email de utilisateur")

    salle = forms.CharField(max_length=20, label="Salle réservée")
    # description = models.fields.CharField(max_length=1000)
    duration = forms.IntegerField(label="Durée de la séance en (H)")
    date_start = forms.DateTimeField(label="Date de début reservation")
    date_end = forms.DateTimeField(label="Date de fin reservation")
    # hour_begin = forms.TimeField( label="Heure de début de la réservation")
    price = forms.IntegerField(label="Montant payé en €")

    # status = models.fields.CharField(choices=Status.choices, max_length=20)

    def __init__(self, *args):
        super(ReservationForm, self).__init__(*args)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
