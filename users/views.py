from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
# 회원가입 view
def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid(): # 유효성 검사
            user = user_form.save(commit=False)   # commit=False --> 바로 저장하지 않고, 임시적으로 저장한다는 뜻.
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/login.html', {'user': user})
    else:
        user_form = RegisterForm()
    return render(request, 'registration/register.html', {'user_form': user_form})
