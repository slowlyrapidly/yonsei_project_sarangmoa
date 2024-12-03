from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}),
        label="비밀번호 확인"
    )

    class Meta:
        model = User
        fields = ['id', 'pw', 'name', 'birth', 'gender', 'address', 'cert_reg_img']
        widgets = {
            'pw': forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
            'id': forms.TextInput(attrs={'placeholder': '아이디'}),
            'uid': forms.NumberInput(attrs={'placeholder': '학번'}),
            'name': forms.TextInput(attrs={'placeholder': '이름'}),
            'birth': forms.NumberInput(attrs={'placeholder': '생년월일 (YYYYMMDD)'}),
            'gender': forms.Select(choices=[('M', '남성'), ('F', '여성')]),
            'address': forms.TextInput(attrs={'placeholder': '주소'}),
        }

    def clean_password_confirm(self):
        pw = self.cleaned_data.get("pw")
        password_confirm = self.cleaned_data.get("password_confirm")
        if pw != password_confirm:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password_confirm

    def clean_id(self):
        id = self.cleaned_data.get("id")
        if User.objects.filter(id=id).exists():
            raise forms.ValidationError("이미 사용 중인 아이디입니다.")
        return id
