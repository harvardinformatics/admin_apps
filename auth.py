from tastypie.authorization import Authorization

class MyAuth(Authorization):
    def is_authorized(self, request, object=None):
        if request.user.date_joined.year == 2010:
            return True
        else:
            return False
        
    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(author__username=request.user.username)
        
        return object_list.none()
