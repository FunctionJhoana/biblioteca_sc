from django import forms
from .models import AuthUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    # Crea el usuario administrador
    
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin_password',
        nombre_1='Nombre',
        apellido_1='Apellido',
        cedula='12345678',
        area=None,
        rol=None
    )
    
    # Agrega el usuario administrador al grupo de administradores
    admin_group = Group.objects.get(name='Administradores')
    admin_group.user_set.add(admin_user)
    # Guarda los cambios en la base de datos
    admin_user.save()
else:
    # El usuario administrador ya existe, no es necesario crearlo
    print("El usuario administrador ya existe.")






class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Ingrese su email'}) )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'*********'
        }
    ))


class RecoverPassword(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Inserte su correo'}) )

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(email=cleaned['email']).exists():
            
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        email = self.cleaned_data.get('email')
        return User.objects.get(email=email)

    # forms.PasswordInput

    # class Meta:
    #     model = AuthUser
    #     fields = ['email', 'password']
    #     widgets = {
    #         'email': forms.EmailField(attrs={'placeholder' : 'Escribe tu correo'}),
    #         'password': forms.PasswordInput(attrs={'placeholder' : 'Escribe tu correo'})
    #     }


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Inserte su contraseña'}) )
    

    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Repita la contraseña'}) )
    
    def clean(self):
        cleaned = super().clean()
        print(cleaned)
        password = cleaned['password']
        confirmpassword = cleaned['confirmpassword']
        if password!=confirmpassword:
            raise forms.ValidationError('Las contraseñas no son iguales')
        return cleaned
