from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import (
    CustomPasswordValidator, error_messages_password, help_text_password,
    CustomPhoneValidator, error_messages_phone
)

"""
Constants
    - Lengths
    - Labels (CustomUser)
    - Labels (CustomGroup)
    - Paths
"""
# Lengths
LENGTH_NAME = 150       # Name field maximum length is 150 (See django.contrib.auth)
LENGTH_PASSWORD = 255   # Password maximum length value is 4096
LENGTH_EMAIL = 254      # Email default length value found on GitHub
LENGTH_PHONE = 10       # Phone number default length value
LENGTH_URL = 200        # URL default length value
LENGTH_TEXT = 5000
LENGTH_GENRE = 100

# Labels (CustomUser)
LABEL_USERNAME = "Nom d'utilisateur"
LABEL_FIRST_NAME = "Prénom"
LABEL_LAST_NAME = "Nom"
LABEL_EMAIL = "Adresse e-mail"
LABEL_PHONE = "Numéro de téléphone"
LABEL_PASSWORD = "Mot de passe"
LABEL_PASSWORD_CURRENT = "Mot de passe actuel"
LABEL_PASSWORD_CONFIRM = "Confirmer le mot de passe"

# Labels (Custom Group)
LABEL_GROUP_NAME = "Nom de groupe"
LABEL_MEMBERS = "Nombre de membres"
LABEL_GENRE = "Style musicale"
LABEL_FACEBOOK = "URL Facebook"
LABEL_INSTAGRAM = "URL Instagram"
LABEL_BIOGRAPHY = "Biographie"
LABEL_TECHNICAL_SHEET = "Fiche technique"
LABEL_LOGO = "Logo"
LABEL_VALIDATED = "Vérifié"

# Paths
MEDIA_PATH = "media/public"



"""
Forms
    - Widgets
    - Forms (CustomUser)
"""
# Widgets
WIDGET_TEXT = forms.TextInput(attrs={'class': 'form-control'})
WIDGET_EMAIL = forms.EmailInput(attrs={'class': 'form-control'})
WIDGET_PASSWORD = forms.PasswordInput(attrs={'class': 'form-control'})

# Forms (CustomUser)
FORM_USERNAME = forms.CharField(max_length=LENGTH_NAME, label=LABEL_USERNAME, widget=WIDGET_TEXT)
FORM_EMAIL = forms.EmailField(max_length=LENGTH_EMAIL, label=LABEL_EMAIL, widget=WIDGET_EMAIL)
FORM_PASSWORD = forms.CharField(label=LABEL_PASSWORD, max_length=LENGTH_PASSWORD, widget=WIDGET_PASSWORD)
FORM_PASSWORD_CONFIRM = forms.CharField(label=LABEL_PASSWORD_CONFIRM, max_length=LENGTH_PASSWORD, widget=WIDGET_PASSWORD)
FORM_PASSWORD_NEW = forms.CharField(label=LABEL_PASSWORD, max_length=LENGTH_PASSWORD, widget=WIDGET_PASSWORD,
                                    validators=CustomPasswordValidator, error_messages=error_messages_password, help_text=help_text_password)

"""
Models
    - Error messages
    - MODEL_GENRE (genres_choices)
    - Models (CustomUser)
    - Models (CustomGroup)
    
"""
# Error messages
UNIQUE_USERNAME = {"unique": "Ce nom d'utilisateur est déjà utilisé"}
UNIQUE_EMAIL = {"unique": "Cette adresse email est déjà utilisée."}

# MODEL_GENRE
genre_choices = [
    ('black metal', 'Black Metal'),
    ('death_metal', 'Death Metal'),
    ('djent', 'Djent'),
    ('doom_metal', 'Doom Metal'),
    ('electro', 'Electro'),
    ('folk_metal', 'Folk Metal'),
    ('hardcore_punk', 'Punk Hardcore'),
    ('heavy_metal', 'Heavy Metal'),
    ('jazz', 'Jazz'),
    ('metal', 'Metal'),
    ('metalcore', 'Metalcore'),
    ('metal_industriel', 'Metal Industriel'),
    ('metal progressif', 'Metal Progressif'),
    ('metal_symphonique', 'Metal Symphonique'),
    ('modern_metal', 'Moderne Metal'),
    ('nu_metal', 'Nu Metal'),
    ('pop', 'Pop'),
    ('pop_rock', 'Pop Rock'),
    ('power_metal', 'Power Metal'),
    ('punk', 'Punk'),
    ('rock', 'Rock'),
    ('rock_alternatif', 'Rock Alternatif'),
    ('rock_progressif', 'Rock Progressif'),
    ('trash_metal', 'Trash Metal'),
]

# CustomUser
MODEL_USERNAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_USERNAME, unique=True, error_messages=UNIQUE_USERNAME)
MODEL_EMAIL = models.EmailField(max_length=LENGTH_EMAIL, verbose_name=LABEL_EMAIL, unique=True, error_messages=UNIQUE_EMAIL)
MODEL_LAST_NAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_FIRST_NAME)
MODEL_FIRST_NAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_LAST_NAME)
MODEL_PHONE = models.CharField(max_length=LENGTH_PHONE, verbose_name=LABEL_PHONE,
                               validators=CustomPhoneValidator, error_messages=error_messages_phone)
MODEL_PASSWORD = models.CharField(max_length=LENGTH_PASSWORD, verbose_name=LABEL_PASSWORD,
                                  validators=CustomPasswordValidator, error_messages=error_messages_password, help_text=help_text_password)
MODEL_PASSWORD_CONFIRM = models.CharField(max_length=LENGTH_PASSWORD, verbose_name=LABEL_PASSWORD_CONFIRM, null=True)

# CustomGroup
MODEL_GROUP_NAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_GROUP_NAME, null=True)
MODEL_GROUP_EMAIL = models.EmailField(max_length=LENGTH_EMAIL, verbose_name=LABEL_EMAIL, null=True)
MODEL_GROUP_PHONE = models.CharField(max_length=LENGTH_PHONE, verbose_name=LABEL_PHONE, null=True,
                                     validators=CustomPhoneValidator, error_messages=error_messages_phone)
MODEL_MEMBERS = models.IntegerField(default=1, verbose_name=LABEL_MEMBERS, null=True)
MODEL_GENRE = models.CharField(max_length=LENGTH_GENRE, choices=genre_choices, null=True)
MODEL_FACEBOOK = models.URLField(max_length=LENGTH_URL, verbose_name=LABEL_FACEBOOK, blank=True, null=True)
MODEL_INSTAGRAM = models.URLField(max_length=LENGTH_URL, verbose_name=LABEL_INSTAGRAM, blank=True, null=True)
MODEL_BIOGRAPHY = models.TextField(max_length=LENGTH_TEXT, verbose_name=LABEL_BIOGRAPHY, blank=True, null=True)
MODEL_TECHNICAL_SHEET = models.FileField(upload_to=MEDIA_PATH, verbose_name=LABEL_TECHNICAL_SHEET, blank=True, null=True)
MODEL_LOGO = models.FileField(upload_to=MEDIA_PATH, verbose_name=LABEL_LOGO, blank=True, null=True)
MODEL_VALIDATED = models.BooleanField(default=False, verbose_name=LABEL_VALIDATED, blank=True, null=True)
