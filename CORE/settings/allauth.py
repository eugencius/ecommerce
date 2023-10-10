ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_MAX_EMAIL_ADDRESSES = 1

# Forms
ACCOUNT_FORMS = {
    # Modified
    "signup": "apps.accounts.forms.SignupForm",
    # Default
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "login": "allauth.account.forms.LoginForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "user_token": "allauth.account.forms.UserTokenForm",
}


# Django allauth - Social account
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {"APP": {"client_id": "123", "secret": "456", "key": ""}},
    "github": {"APP": {"client_id": "123", "secret": "456", "key": ""}},
}

# Backend authentications
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
