from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from tastypie.models import ApiKey
from models import DjelmahLog

# LOGS

@require_GET
def index(request):
    return HttpResponseRedirect('/djelmah/logs')

@require_GET
def log_index(request):
    logs = DjelmahLog.objects.all().order_by('-datetime')
    return render(request, 'djelmah/logs.html', { 'logs': logs })

@require_GET
def log_detail(request, log_id):
    log = get_object_or_404(DjelmahLog, pk=log_id)
    return HttpResponse(log.raw_html)

@require_POST
def delete_log(request):
    log_id = request.POST['log_id']
    log = get_object_or_404(DjelmahLog, pk=log_id)

    log.delete()

    return HttpResponse()

@require_GET
def log_test(request):
    raise Exception("It Works!")

# API KEYS

@require_GET
def api_keys(request):
    keys = ApiKey.objects.all().order_by('user__username')
    users = User.objects.exclude(
        id__in=keys.values_list('user_id', flat=True)
    ).order_by('last_name', 'first_name')

    context = {
        'keys': keys,
        'users': users,
    }

    return render(request, 'djelmah/keys.html', context)

@require_POST
def create_api_key(request):
    user_id = request.POST['user_id']
    user = get_object_or_404(User, pk=user_id)

    key, created = ApiKey.objects.update_or_create(
        user=user, defaults={ 'key': None }
    )

    return HttpResponse()

@require_POST
def revoke_api_key(request):
    key_id = request.POST['key_id']
    key = get_object_or_404(ApiKey, pk=key_id)

    key.delete()

    return HttpResponse()
