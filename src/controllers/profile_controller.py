from views.profile_view import ProfileView

class ProfileController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.profile_view = ProfileView(self)
    
    def show_profile(self):
        self.profile_view.build()
    
    def logout(self):
        self.app.logout()