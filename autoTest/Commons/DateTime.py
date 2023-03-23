import time
from datetime import date, datetime, timedelta

class DataTime(object):
    @staticmethod
    def GetTime():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def Get_Current_Time_Format(date_format="%Y-%m-%d %H:%M:%S"):
        return datetime.now().strftime(date_format)

    @staticmethod
    def Get_Current_Date(date_format="%Y-%m-%d"):
        """Get the current date with date format

        Example:
        | Get Current Date |
        """
        return date.today().strftime(date_format)

    @staticmethod
    def Get_Current_Year():
        """Get the current year.

        Example:
        | Get Current Year |
        """
        return date.today().year

    @staticmethod
    def Get_Current_Month():
        """Get the current month.

        Example:
        | Get Current Month |
        """
        return date.today().month

    @staticmethod
    def Get_Current_Day():
        return date.today().day

    def get_dif_time(time1, time2):
        a1 = datetime.now().strptime(time1, "%Y-%m-%d %H:%M:%S")
        a2 = datetime.now().strptime(time2, "%Y-%m-%d %H:%M:%S")
        return (a1-a2).seconds


    def Set_Time(self, t):
        """Set the system time"""
        self.logger.log_info("Set the time to '%s'" % str(t))

        try:
            cmd = "time " + t
            self.com.run_command_as_admin(cmd)
        except Exception:
            self.logger.log_warn(Exception.message)
        time.sleep(5)
        # self.com.verify(time.strftime("%H:%M"), str(t)[0:5])

    @staticmethod
    def Get_Date_X_Number_Of_Days(numdays, format="%Y-%m-%d"):
        """
        Takes a number of days and returns a date with format
        that represents today minus that number of days.
        Example:
        | Get Date X Number Of Days | 5 |
        | Get Date X Number Of Days | -5 |
        | Get Date X Number Of Days | 5 | %Y%m%d |

        Takes a number of days and returns a date in MM/DD/YYYY format
        that represents today minus that number of days.
        :arg
            numdays: days after today, int or string format integer. e.g. 7, "10"
                     days before today, int or string format integer. e.g. -7, "-10"
        :rtype
            string
        :usage
            one_week_ago = self.get_date_x_number_of_days(-7)
        """
        date = datetime.now() + timedelta(days=int(numdays))
        return date.strftime(format)

    def Get_Date_X_Number_Of_Months(self, nummonths, format="%m/%d/%Y"):
        """
        Takes a number of months and returns a date with format
        that represents today minus that number of days.
        Example:
        | Get Date X Number Of Months | 5 |
        | Get Date X Number Of Months | -5 |
        | Get Date X Number Of Months | 5 | %Y%m%d |

        Takes a number of months and returns a date in MM/DD/YYYY format
        that represents today minus that number of months.
        :arg
            nummonths: months after today, int or string format integer. e.g. 7, "10"
                       months before today, int or string format integer. e.g. -7, "-10"
        :rtype
            string
        :usage
            one_week_ago = self.get_date_x_number_of_months(-7)
        """
        date = datetime.now()
        nummonths = int(nummonths)
        m, y = (date.month + nummonths) % 12, date.year + ((date.month) + nummonths - 1) // 12
        if not m: m = 12
        d = min(date.day, [31,
                           29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][
            m - 1])
        date = date.replace(day=d, month=m, year=y)
        return date.strftime(format)

    def Get_Date_X_Number_Of_Years(self, numyears, format="%m/%d/%Y"):
        """
        Takes a number of months and returns a date with format
        that represents today minus that number of days.
        Example:
        | Get Date X Number Of Months | 5 |
        | Get Date X Number Of Months | -5 |
        | Get Date X Number Of Months | 5 | %Y%m%d |

        Takes a number of years and returns a date in MM/DD/YYYY format
        that represents today minus that number of years.
        :arg
            numyears: years after today, int or string format integer. e.g. 7, "10"
                       years before today, int or string format integer. e.g. -7, "-10"
        :usage
            one_week_ago = self.get_date_x_number_of_years(-7)
        """
        date = datetime.now()
        numyears = int(numyears)
        d, m, y = date.day, date.month, date.year + numyears
        date = date.replace(day=d, month=m, year=y)
        return date.strftime(format)

    def Get_Time_X_Number_Of_Seconds(self, seconds):
        """
        Takes a number of seconds and returns time in HH:MM:SS format
        """
        time = datetime.now() + timedelta(seconds=int(seconds))
        return time.strftime("%H:%M:%S")

    def Get_Time_X_Number_Of_Hours(self, hours):
        """
        Takes a number of hours and returns time in HH:MM:SS format
        """
        time = datetime.now() + timedelta(hours=int(hours))
        return time.strftime("%H:%M:%S")

    def Get_Time_X_Number_Of_Minutes(self, minutes):
        """
        Takes a number of minutes and returns time in HH:MM:SS format
        """
        time = datetime.now() + timedelta(minutes=int(minutes))
        return time.strftime("%H:%M:%S")

    def Convert_Date_To_Different_Format(self, date_string, format):
        """Converts the specified date in format mm/dd/yyyy to the specified format.  Initial format must be mm/dd/yyyy.

        Example:
        | Convert Date To Different Format | 11/11/2000 | %d/%m/%Y |
        | Convert Date To Different Format | 11/11/2000 | %Y/%d/%m |
        """
        date_object = datetime.strptime(date_string, '%m/%d/%Y')
        return date_object.strftime(format)


    def wait_time_sec(self, DateTime):
        Sec = DateTime.second
        if 57 <= int(Sec) <= 59:
            time.sleep(2)
            self.logger.log_info_green("Time second between 57 to 59,wait 2 sec.")
            return datetime.now()
        else:
            return DateTime

