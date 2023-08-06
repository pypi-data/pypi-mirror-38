from Zope2 import zpublisher_exception_hook
from Zope2 import zpublisher_transactions_manager
from Zope2 import bobo_application
from Zope2 import __bobo_before__
from AccessControl.SpecialUsers import system
from AccessControl.SecurityManagement import newSecurityManager

def zpublisher_validated_hook(request, user):
    newSecurityManager(request, system)
