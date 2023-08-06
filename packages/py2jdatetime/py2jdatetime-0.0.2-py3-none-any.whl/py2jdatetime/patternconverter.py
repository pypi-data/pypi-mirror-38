from functools import reduce
from py2jdatetime.constants import JavaStandard as Java, CStandard as C


class PatternConverter:
    DIRECTIVE_MAP = {
        C.DAY_OF_MONTH: Java.DAY_OF_MONTH * Java.NUMBER_TWO_PADDING,
        C.YEAR_FULL_FORM: Java.YEAR * Java.YEAR_FULL_FORM,
        C.YEAR_SHORT_FROM: Java.YEAR * Java.YEAR_REDUCED_FORM,
        C.MONTH_FULL_FORM: Java.MONTH_OF_YEAR * Java.TEXT_FULL_FORM,
        C.MONTH_SHORT_FORM: Java.MONTH_OF_YEAR * Java.TEXT_SHORT_FORM,
        C.MONTH_NUMBER_FROM: Java.MONTH_OF_YEAR * Java.NUMBER_TWO_PADDING,
        C.HOUR_OF_DAY: Java.HOUR_OF_DAY * Java.NUMBER_TWO_PADDING,
        C.MINUTE_OF_HOUR: Java.MINUTE_OF_HOUR * Java.NUMBER_TWO_PADDING,
        C.SECOND_OF_MINUTE: Java.SECOND_OF_MINUTE * Java.NUMBER_TWO_PADDING,
        C.MILLISECOND: '',
        C.DAY_OF_WEEK_SHORT_FORM: Java.DAY_OF_WEEK * Java.TEXT_SHORT_FORM,
        C.DAY_OF_WEEK_FULL_FORM: Java.DAY_OF_WEEK * Java.TEXT_FULL_FORM,
        C.DAY_OF_WEEK_NUMBER_FORM: Java.DAY_OF_WEEK * Java.NUMBER_NO_PADDING,
        C.CLOCK_HOUR_OF_AM_PM: Java.CLOCK_HOUR_OF_AM_PM * Java.NUMBER_TWO_PADDING,
        C.AM_PM_OF_DAY: Java.AM_PM_OF_DAY,
        C.TIMEZONE_NAME: Java.TIME_ZONE_NAME * Java.ZONE_NAME_SHORT_FORM,
        C.UTC_OFFSET: '',
        C.DAY_OF_YEAR: Java.DAY_OF_YEAR * Java.NUMBER_THREE_PADDING,
        C.WEEK_OF_YEAR: Java.WEEK_OF_YEAR * Java.NUMBER_TWO_PADDING,
        C.WEEK_OF_YEAR_MONDAY: ''
    }

    def convert_to_iso_8601(self, pattern):
        return reduce(lambda a, kv: a.replace(*kv), self.DIRECTIVE_MAP.items(), pattern)
