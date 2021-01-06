from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Account, Day
from .forms import AccountForm


@login_required
def account_router(request: HttpRequest):
    account = Account.default_for_user(request.user)
    if account:
        return redirect(day_router, account.id)
    else:
        return redirect(new_account)


@login_required
def new_account(request: HttpRequest):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect(feature_router, account.id)
    else:
        form = AccountForm()
    return render(
        request, 'calc/edit_account.html', {'form': form, 'role': "Add account"}
    )


@login_required
def select_account(request: HttpRequest):
    accounts = Account.objects.filter(user=request.user)
    if accounts.exists():
        return render(request, 'calc/select_account.html', {'accounts': accounts})
    else:
        return redirect(new_account)


@login_required
def day_router(request: HttpRequest, account_id: int):
    return redirect('feature_router', account_id, Day.today())


@login_required
def feature_router(request: HttpRequest, account_id: int, day: Day):
    return redirect(speedups, account_id, day)


@login_required
def speedups(request: HttpRequest, account_id: int, day: Day):
    account = get_object_or_404(Account, id=account_id)
    return render(request, 'calc/speedups.html', {'account': account, 'day': day})


def login_form(request):
    context = {}
    if settings.DEBUG:
        if 'du' in request.GET:
            try:
                user = User.objects.get_by_natural_key(request.GET['du'])
                login(request, user)
                return redirect(request.GET['next'])
            except User.DoesNotExist:
                return redirect('login')
        context['dev_accounts'] = User.objects.all()
    return render(request, 'login.html', context)
