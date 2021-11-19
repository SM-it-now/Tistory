from django import forms
from .models import User

# 회원가입 폼
class RegisterForm(forms.ModelForm):
    # widget은 장고에서의 HTML 입력요소를 말한다.
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'gender', 'email']

    # 비밀번호의 유효성 검사.
    # clean_메서드 (메서드 = 필드 네임) --> clean() 함수.
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다!')

        return cd['confirm_password']
