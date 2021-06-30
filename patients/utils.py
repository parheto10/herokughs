# calendarapp/utils.py
# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Patient, Rdv
#from eventcalendar.helper import get_current_user


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, rdvs):
        rdvs_per_day = rdvs.filter(date_rdv__day=day)
        d = ''

        for rdv in rdvs_per_day:
            d += f'<li> {rdv.get_html_url} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, rdvs):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, rdvs)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        rdvs = Rdv.objects.filter(date_rdv__year=self.year, date_rdv__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, rdvs)}\n'
        return cal