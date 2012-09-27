from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frittie.app.info.views',
   url(r"^about_us", "about_us"),
   url(r"^contact_us", "contact_us"),
   url(r"^copyright", "copyright"),
   url(r"^career","career"),
   url(r"^help", "help_page"),
   url(r"^privacy_policy", "privacy_policy"),
   url(r"^team", "team"),
   url(r"^term_service", "term_service"),
   url(r"^safety","safety"),
)
