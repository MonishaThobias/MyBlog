from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost, Subscriber

# --- Sign Up Form ---
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            
# --- Blog Post Form ---
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter blog title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your blog content here...',
                'class': 'form-control',
                'rows': 5
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

# --- Subscriber Form ---
class SubscriberForm(forms.ModelForm):
    subscribe = forms.BooleanField(
        required=True,
        label="Yes, Subscribe me to your newsletter"
    )

    class Meta:
        model = Subscriber
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email to subscribe',
            'class': 'form-control'
        })

    def clean_subscribe(self):
        subscribe = self.cleaned_data.get('subscribe')
        if not subscribe:
            raise forms.ValidationError("You must agree to subscribe.")
        return subscribe
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email address already in use.")
            return email
