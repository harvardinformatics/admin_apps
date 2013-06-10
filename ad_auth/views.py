import urlparse

from django.conf import settings
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm


from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sites.models import get_current_site

#from ad_auth.auth import ActiveDirectoryBackend
#from ad_auth.auth.ActiveDirectoryBackend import authenticate

@sensitive_post_parameters()
@csrf_exempt
#@never_cache
def login_view(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        #adb = ActiveDirectoryBackend()
        user = authenticate(username=username,password=password)
        dd = {}
        if user is not None:
            if user.is_active:
                netloc = urlparse.urlparse(redirect_to)[1]
                # Use default setting if redirect_to is empty
                if not redirect_to:
                    redirect_to = settings.LOGIN_REDIRECT_URL

                # Heavier security check -- don't allow redirection to a different
                # host.
                elif netloc and netloc != request.get_host():
                    redirect_to = settings.LOGIN_REDIRECT_URL

                # Okay, security checks complete. Log the user in.
                auth_login(request,user)

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                return HttpResponseRedirect(redirect_to)

            else:
                dd.update({'error': 'not_active'})

        else:
            # Return an 'invalid login' error message.
            dd.update({'error': 'bad_user'})
        return render_to_response("registration/login.html",
                                  dd,
                                  context_instance=RequestContext(request))
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def logout_page(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')
