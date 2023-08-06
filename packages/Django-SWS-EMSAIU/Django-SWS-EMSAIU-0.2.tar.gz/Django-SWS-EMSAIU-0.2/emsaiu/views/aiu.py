import logging
import os
from time import strftime, tzset

from authz_group import Group
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from restclients_core.exceptions import DataFailureException
from userservice.user import UserService
from uw_sws.term import get_current_term

from emsaiu.exceptions import StudentWebServiceUnavailable

logger = logging.getLogger(__name__)


@login_required
def index(request, template='emsaiu/aiu.html'):
    user = request.user.username
    if not Group().is_member_of_group(user, settings.EMSTOOLS_SCHEDULER_GROUP):
        return HttpResponseRedirect("/")

    status_code = 200

    try:
        term = get_current_term()
    except DataFailureException as ex:
        logger.exception(ex)
        raise StudentWebServiceUnavailable()

    os.environ['TZ'] = 'America/Los_Angeles'
    tzset()

    context = {
        'term_year': term.year,
        'term_quarter': term.quarter,
        'todays_date': strftime("%Y-%m-%d"),
        'STATIC_URL': settings.STATIC_URL,
    }

    return render(request, template, context, status=status_code)
