from django.utils.translation import ugettext as _


"""
Custom exceptions used by AIU.
"""


class InvalidUser(Exception):
    pass


class StudentWebServiceUnavailable(Exception):
    def __str__(self):
        return _("sws_not_available")
