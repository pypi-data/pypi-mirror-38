import logging
import re
from datetime import datetime, timedelta

from ems_client.service import Service
from uw_sws.section import (get_section_by_url,
                            get_sections_by_building_and_term)
from uw_sws.term import get_term_by_year_and_quarter


class CourseEventException(Exception):
    pass


logger = logging.getLogger(__name__)


def aiu_record_from_meeting(meeting):
    record = {
        'Department': meeting.section.curriculum_abbr,
        'Course': meeting.section.course_number,
        'Section': meeting.section.section_id,
        'CourseTitle': meeting.section.course_title,
        'Instructor': "",
        'Days': "",
        'Building': meeting.building,
        'Room': meeting.room_number,
        'BegTime': meeting.start_time.replace(':', ''),
        'EndTime': meeting.end_time.replace(':', ''),
        'StartDate': (meeting.section.start_date or
                      meeting.term.first_day_quarter),
        'EndDate': (meeting.section.end_date or
                    meeting.term.last_day_instruction),
        'Attendance': None,
    }

    if meeting.section.summer_term == 'A-term':
        record['EndDate'] = meeting.term.aterm_last_date
    if meeting.section.summer_term == 'B-term':
        record['StartDate'] = meeting.term.bterm_first_date

    for instructor in meeting.instructors:
        if instructor.TSPrint:
            record['Instructor'] = instructor.display_name
    if meeting.instructors and not record['Instructor']:
        record['Instructor'] = meeting.instructors[0].display_name
    if not record['Instructor']:
        record['Instructor'] = "UNK"

    if meeting.meets_monday:
        record['Days'] += 'M'
    if meeting.meets_tuesday:
        record['Days'] += 'T'
    if meeting.meets_wednesday:
        record['Days'] += 'W'
    if meeting.meets_thursday:
        record['Days'] += 'Th'
    if meeting.meets_friday:
        record['Days'] += 'F'
    if meeting.meets_saturday:
        record['Days'] += 'Sa'
    if meeting.meets_sunday:
        record['Days'] += 'Su'

    return record


def aiu_record_from_section_final(section):
    record = {
        'Department': section.curriculum_abbr,
        'Course': section.course_number,
        'Section': section.section_id,
        'CourseTitle': "%s/FINAL" % section.course_title,
        'Instructor': "UNK",
        'Days': "",
        'Building': section.final_exam.building,
        'Room': section.final_exam.room_number,
        'BegTime': section.final_exam.start_date.strftime('%H%M'),
        'EndTime': section.final_exam.end_date.strftime('%H%M'),
        'StartDate': section.final_exam.start_date.date(),
        'EndDate': section.final_exam.end_date.date(),
        'Attendance': None,
    }
    days = ['Su', 'M', 'T', 'W', 'Th', 'F', 'Sa']
    record['Days'] = days[int(section.final_exam.start_date.strftime('%w'))]

    return record


def get_aiu_data_for_term(term):
    if not term.first_day_quarter:
        term = get_term_by_year_and_quarter(term.year, term.quarter)

    _ems = Service()

    buildings = _ems.get_buildings()

    rooms = _ems.get_all_rooms()
    roomlist = [room.description for room in rooms]

    meetings = []
    for building in buildings:
        sectionlist = get_sections_by_building_and_term(
            building.building_code, term)
        for section in sectionlist:
            section = get_section_by_url(section.url)
            for meeting in section.meetings:
                if meeting.building_to_be_arranged or \
                        meeting.room_to_be_arranged or \
                        meeting.days_to_be_arranged:
                    continue

                if "%s %s" % (meeting.building, meeting.room_number) in \
                        roomlist:
                    meetings.append(aiu_record_from_meeting(meeting))

            if section.final_exam and \
                    section.final_exam.building and \
                    section.final_exam.room_number and \
                    section.final_exam.start_date and \
                    section.final_exam.end_date and \
                    section.final_exam.room_number != '*' and \
                    "%s %s" % (section.final_exam.building,
                               section.final_exam.room_number) in roomlist:
                meetings.append(aiu_record_from_section_final(section))

    term_data = term.json_data()
    # hack. we want a date, not a datetime
    term_data['last_final_exam_date'] = str(term.last_final_exam_date)

    return {
        'term': term_data,
        'records': meetings,
    }
