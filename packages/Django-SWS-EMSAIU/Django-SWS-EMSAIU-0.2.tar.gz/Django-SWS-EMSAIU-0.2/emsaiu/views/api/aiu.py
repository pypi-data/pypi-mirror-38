import logging

from restclients_core.exceptions import DataFailureException

from emsaiu.utils import CourseEventException, get_aiu_data_for_term
from emsaiu.utils.validation import Validation
from emsaiu.views.api.exceptions import (InvalidParamException,
                                         MissingParamException)
from emsaiu.views.rest_dispatch import RESTDispatch

logger = logging.getLogger(__name__)


class AIU(RESTDispatch):
    def GET(self, request, **kwargs):
        format = kwargs.get('format', 'json')

        try:
            term = Validation().term_id(kwargs['term_id'])
            data = get_aiu_data_for_term(term)
        except MissingParamException as ex:
            return self.error_response(400, message=str(ex))
        except CourseEventException as ex:
            return self.error_response(404, message=str(ex))
        except InvalidParamException as ex:
            return self.error_response(400, message=str(ex))
        except DataFailureException as ex:
            return self.error_response(ex.status, str(ex))
        except Exception as ex:
            logger.exception(ex)
            return self.error_response(500, str(ex))

        if format == 'txt':
            response = self.tsv_response(data['records'], fields=[
                'Department',
                'Course',
                'Section',
                'CourseTitle',
                'Instructor',
                'Days',
                'Building',
                'Room',
                'BegTime',
                'EndTime',
                'StartDate',
                'EndDate',
                'Attendance',
            ])

            # response['Content-Disposition'] = \
            #     'attachment; filename="%s"' % filename
            return response

        return self.json_response(data)
