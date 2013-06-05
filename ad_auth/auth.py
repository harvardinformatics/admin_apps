import sys, os, re

root_path = os.path.abspath(os.path.split(__file__)[0])
APPLICATION_ROOT = os.path.realpath(os.path.join(root_path, '.'))
sys.path.insert(0, APPLICATION_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_apps.settings.local'

from django.contrib.auth.models import User
from admin_apps.settings import local
import ldap

ldap.set_option(ldap.OPT_REFERRALS, 0)
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

LDAP_SERVER = 'ldaps://10.242.26.103:636'
AD_BIND_DN = 'account@rc.domain'
AD_BIND_PW = 'Formula350!'
DOMAIN_STRING = 'rc.domain'
BASE_DOMAIN = 'ou=Domain Users,dc=rc,dc=domain'
GROUP_DOMAIN = 'ou=Domain Groups,dc=rc,dc=domain'

class ActiveDirectoryBackend:

  def authenticate(self,username=None,password=None):
    if not self.is_valid(username,password):
      return None
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      l = ldap.initialize(LDAP_SERVER)
      l.simple_bind_s(username,password)
      result = l.search_ext_s(BASE_DOMAIN,
                              ldap.SCOPE_SUBTREE, 
                              "sAMAccountName=%s" % username,
                              "[*]")[0][1]
      l.unbind_s()

      # givenName == First Name
      if result.has_key('givenName'):
        first_name = result['givenName'][0]
      else:
        first_name = None

      # sn == Last Name (Surname)
      if result.has_key('sn'):
        last_name = result['sn'][0]
      else:
        last_name = None

      # mail == Email Address
      if result.has_key('mail'):
        email = result['mail'][0]
      else:
        email = None

      user = User(username=username,first_name=first_name,last_name=last_name,email=email)
      user.is_staff = False
      user.is_superuser = False
      user.set_unusable_password()
      user.save()
    return user

  def get_user(self,user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None

  def is_valid (self,username=None,password=None):
    ## Disallowing null or blank string as password
    ## as per comment: http://www.djangosnippets.org/snippets/501/#c868
    if password == None or password == '':
      return False
    binddn = "%s@%s" % (username,DOMAIN_STRING)
    try:
      l = ldap.initialize(LDAP_SERVER)
      l.simple_bind_s(binddn,password)
      #print "is valid user from AD!"
      l.unbind_s()
      return True
    except ldap.LDAPError:
      return False


if __name__=='__main__':
  l = ActiveDirectoryBackend()
  print l.authenticate('emattison','asdf')
  sys.exit()
  
