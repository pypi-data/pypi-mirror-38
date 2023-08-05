# -*- coding: utf-8 -*-

"""
Jewish calendrical date and times for a given location.

HDate calculates and generates a represantation either in English or Hebrew
of the Jewish calendrical date and times for a given location
"""
from __future__ import division

import datetime
import logging
import sys
from itertools import chain, product

from hdate import converters as conv
from hdate import htables
from hdate.common import HebrewDate, set_date

_LOGGER = logging.getLogger(__name__)


class HDate(object):  # pylint: disable=useless-object-inheritance
    """
    Hebrew date class.

    Supports converting from Gregorian and Julian to Hebrew date.
    """

    def __init__(self, date=None, diaspora=False, hebrew=True):
        """Initialize the HDate object."""
        self._hdate = None
        self._gdate = None
        self._last_updated = None
        self.hebrew = hebrew
        self.diaspora = diaspora
        self.gdate = date
        self.hdate = None

    def __unicode__(self):
        """Return a Unicode representation of HDate."""
        return get_hebrew_date(self.hdate, self.get_omer_day(), self.dow,
                               self.holiday_description, hebrew=self.hebrew,
                               short=False)

    def __str__(self):
        """Return a string representation of HDate."""
        if sys.version_info.major < 3:
            # pylint: disable=undefined-variable
            return unicode(self).encode('utf-8')  # noqa: F821

        return self.__unicode__()

    @property
    def hdate(self):
        """Return the hebrew date."""
        if self._last_updated == "hdate":
            return self._hdate
        return conv.jdn_to_hdate(self._jdn)

    @hdate.setter
    def hdate(self, date):
        """Set the dates of the HDate object based on a given Hebrew date."""
        # Sanity checks
        if date is None and isinstance(self.gdate, datetime.date):
            date = self.hdate

        if not 0 < date.month < 15:
            raise ValueError(
                'month ({}) legal values are 1-14'.format(date.month))
        if not 0 < date.day < 31:
            raise ValueError('day ({}) legal values are 1-31'.format(date.day))
        if not isinstance(date, HebrewDate):
            raise TypeError('date: {} is not of type HebrewDate'.format(date))

        self._last_updated = "hdate"
        self._hdate = date

    @property
    def gdate(self):
        """Return the Gregorian date for the given Hebrew date object."""
        if self._last_updated == "gdate":
            return self._gdate
        return conv.jdn_to_gdate(self._jdn)

    @gdate.setter
    def gdate(self, date):
        """Set the Gregorian date for the given Hebrew date object."""
        self._last_updated = "gdate"
        self._gdate = set_date(date)

    @property
    def _jdn(self):
        """Return the Julian date number for the given date."""
        if self._last_updated == "gdate":
            return conv.gdate_to_jdn(self.gdate)
        return conv.hdate_to_jdn(self.hdate)

    @property
    def hebrew_date(self):
        """Return the hebrew date string."""
        return u"{} {} {}".format(
            hebrew_number(self.hdate.day, hebrew=self.hebrew),   # Day
            htables.MONTHS[self.hdate.month - 1][self.hebrew],   # Month
            hebrew_number(self.hdate.year, hebrew=self.hebrew))  # Year

    @property
    def parasha(self):
        """Return the upcoming parasha."""
        return htables.PARASHAOT[self.get_reading()][self.hebrew]

    @property
    def holiday_description(self):
        """
        Return the holiday description.

        In case none exists will return None.
        """
        entry = self._holiday_entry()
        desc = entry.description
        return desc.hebrew.long if self.hebrew else desc.english

    @property
    def holiday_type(self):
        """Return the holiday type if exists."""
        entry = self._holiday_entry()
        return entry.type

    def _holiday_entry(self):
        """Return the number of holyday."""
        # Get the possible list of holydays for this day
        holydays_list = [
            holyday for holyday in htables.HOLIDAYS if
            (self.hdate.day, self.hdate.month) in product(
                *([x] if isinstance(x, int) else x for x in holyday.date))]

        # Filter any non-related holydays depending on Israel/Diaspora only
        holydays_list = [
            holyday for holyday in holydays_list if
            (holyday.israel_diaspora == "") or
            (holyday.israel_diaspora == "ISRAEL" and not self.diaspora) or
            (holyday.israel_diaspora == "DIASPORA" and self.diaspora)]

        # Filter any special cases defined by True/False functions
        holydays_list = [
            holyday for holyday in holydays_list if
            all(func(self) for func in holyday.date_functions_list)]

        assert len(holydays_list) <= 1

        # If anything is left return it, otherwise return the "NULL" holiday
        return holydays_list[0] if holydays_list else htables.HOLIDAYS[0]

    def short_kislev(self):
        """Return whether this year has a short Kislev or not."""
        return True if self.year_size() in [353, 383] else False

    @property
    def dow(self):
        """Return Hebrew day of week Sunday = 1, Saturday = 6."""
        return self.gdate.weekday() + 2 if self.gdate.weekday() != 6 else 1

    def year_size(self):
        """Return the size of the given Hebrew year."""
        return conv.get_size_of_hebrew_year(self.hdate.year)

    def rosh_hashana_dow(self):
        """Return the Hebrew day of week for Rosh Hashana."""
        jdn = conv.hdate_to_jdn(HebrewDate(self.hdate.year, 1, 1))
        return (jdn + 1) % 7 + 1

    def pesach_dow(self):
        """Return the first day of week for Pesach."""
        jdn = conv.hdate_to_jdn(HebrewDate(self.hdate.year, 7, 15))
        return (jdn + 1) % 7 + 1

    def get_omer_day(self):
        """Return the day of the Omer."""
        first_omer_day = HebrewDate(self.hdate.year, 7, 16)
        omer_day = self._jdn - conv.hdate_to_jdn(first_omer_day) + 1
        if not 0 < omer_day < 50:
            return 0
        return omer_day

    def get_reading(self):
        """Return number of hebrew parasha."""
        _year_type = (self.year_size() % 10) - 3
        year_type = (
            self.diaspora * 1000 +
            self.rosh_hashana_dow() * 100 +
            _year_type * 10 +
            self.pesach_dow())

        _LOGGER.debug("Year type: %d", year_type)

        # Number of days since rosh hashana
        rosh_hashana = HebrewDate(self.hdate.year, 1, 1)
        days = self._jdn - conv.hdate_to_jdn(rosh_hashana)
        # Number of weeks since rosh hashana
        weeks = (days + self.rosh_hashana_dow() - 1) // 7
        _LOGGER.debug("Days: %d, Weeks %d", days, weeks)

        if weeks == 3:
            if (days <= 22 and self.diaspora and self.dow != 7 or
                    days <= 21 and not self.diaspora):
                return 54

        # Special case
        if weeks == 4 and days == 22 and self.diaspora:
            return 54

        # Return the indexes for the readings of the given year
        readings = list(
            chain(*([x] if isinstance(x, int) else x
                    for reading in htables.READINGS
                    for x in reading.readings
                    if year_type in reading.year_type)))

        return readings[weeks]


def hebrew_number(num, hebrew=True, short=False):
    """Return "Gimatria" number."""
    if not hebrew:
        return str(num)
    if not 0 <= num < 10000:
        raise ValueError('num must be between 0 to 9999, got:{}'.format(num))
    hstring = u""
    if num >= 1000:
        hstring += htables.DIGITS[0][num // 1000]
        hstring += u"' "
        num = num % 1000
    while num >= 400:
        hstring += htables.DIGITS[2][4]
        num = num - 400
    if num >= 100:
        hstring += htables.DIGITS[2][num // 100]
        num = num % 100
    if num >= 10:
        if num in [15, 16]:
            num = num - 9
        hstring += htables.DIGITS[1][num // 10]
        num = num % 10
    if num > 0:
        hstring += htables.DIGITS[0][num]
    # possibly add the ' and " to hebrew numbers
    if not short:
        if len(hstring) < 2:
            hstring += u"'"
        else:
            hstring = hstring[:-1] + u'"' + hstring[-1]
    return hstring


def get_omer_string(omer):
    """Return a string representing the count of the Omer."""
    tens = [u"", u"עשרה", u"עשרים", u"שלושים", u"ארבעים"]
    ones = [u"", u"אחד", u"שנים", u"שלושה", u"ארבעה", u"חמשה",
            u"ששה", u"שבעה", u"שמונה", u"תשעה"]
    if not 0 < omer < 50:
        raise ValueError('Invalid Omer day: {}'.format(omer))
    ten = omer // 10
    one = omer % 10
    omer_string = u'היום '
    if 10 < omer < 20:
        omer_string += ones[one] + u' עשר'
    elif omer > 9:
        omer_string += ones[one]
        if one:
            omer_string += u' ו'
    if omer > 2:
        if omer > 20 or omer in [10, 20]:
            omer_string += tens[ten]
        if omer < 11:
            omer_string += ones[one] + u' ימים '
        else:
            omer_string += u' יום '
    elif omer == 1:
        omer_string += u'יום אחד '
    else:  # omer == 2
        omer_string += u'שני ימים '
    if omer > 6:
        omer_string += u'שהם '
        weeks = omer // 7
        days = omer % 7
        if weeks > 2:
            omer_string += ones[weeks] + u' שבועות '
        elif weeks == 1:
            omer_string += u'שבוע אחד '
        else:  # weeks == 2
            omer_string += u'שני שבועות '
        if days:
            omer_string += u'ו'
            if days > 2:
                omer_string += ones[days] + u' ימים '
            elif days == 1:
                omer_string += u'יום אחד '
            else:  # days == 2
                omer_string += u'שני ימים '
    omer_string += u'לעומר'
    return omer_string


def get_hebrew_date(date, omer=0, dow=0, holiday_desc="",
                    short=False, hebrew=True):
    """Return a string representing the given date."""
    # Day
    res = u"{} {}".format(hebrew_number(date.day, hebrew=hebrew, short=short),
                          u"ב" if hebrew else u"")
    # Month
    res += htables.MONTHS[date.month - 1][hebrew]
    # Year
    res += u" " + hebrew_number(date.year, hebrew=hebrew, short=short)

    # Weekday
    if dow:
        dw_str = u"יום " if hebrew else u""
        dw_str += htables.DAYS[dow - 1][hebrew][short]
        res = dw_str + u" " + res
    if short:
        return res

    # Omer
    if 0 < omer < 50:
        res += u" " + hebrew_number(omer, hebrew=hebrew, short=short)
        res += u" " + u"בעומר" if hebrew else u" in the Omer"

    # Holiday
    if holiday_desc:
        res += u" " + holiday_desc
    return res
