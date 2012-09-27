from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from frittie.helper.settings_helper import SESSION_KEY

class CustomAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if SESSION_KEY in request.session:
            return True
        else:
            return False
