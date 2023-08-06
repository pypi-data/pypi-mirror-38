import re

from uw_sws.models import Term

from emsaiu.views.api.exceptions import (InvalidParamException,
                                         MissingParamException)


class ValidationException(Exception):
    pass


class Validation(object):
    """  Validates various parameters and such
    """

    def term_id(self, term_id):
        if not term_id:
            raise MissingParamException('missing term id')

        term_parts = re.match(
            r'^(\d{4})-(winter|spring|summer|autumn)$', term_id, re.I)
        if not term_parts:
            raise InvalidParamException('invalid term id: %s' % term_id)

        term = Term()
        term.year = term_parts.group(1)
        term.quarter = term_parts.group(2).lower()
        return term
