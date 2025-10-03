from datetime import datetime, timedelta
import pytz
from flask import request
import requests


class FormatTime:
    
    @staticmethod
    def format_message_time(dt_str, tz='Asia/Kolkata'):
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        local_tz = pytz.timezone(tz)
        dt = dt.replace(tzinfo=pytz.utc).astimezone(local_tz)

        now = datetime.now(local_tz)
        dt_date = dt.date()
        now_date = now.date()
        days_diff = (now_date - dt_date).days
        time_str = dt.strftime("%-I:%M %p")  # "5:22 AM"

        if days_diff == 0:
            return f"{time_str}"
        elif days_diff == 1:
            return f"Yesterday at {time_str}"
        elif 1 < days_diff <= 7:
            return f"{days_diff} days ago at {time_str}"
        elif dt.year == now.year:
            return f"{dt.strftime('%b %-d')} at {time_str}"
        else:
            return f"{dt.strftime('%b %-d, %Y')} at {time_str}"

    @staticmethod
    def format_time(dt_str, tz='Asia/Kolkata'):
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        local_tz = pytz.timezone(tz)
        dt = dt.replace(tzinfo=pytz.utc).astimezone(local_tz)

        now = datetime.now(local_tz)
        delta = now - dt

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = delta.days
        weeks = days // 7

        if seconds < 60:
            return "Just now"
        elif minutes < 60:
            return f"{int(minutes)} minute{'s' if minutes > 1 else ''} ago"
        elif hours < 24:
            return f"{int(hours)} hour{'s' if hours > 1 else ''} ago"
        elif days < 7:
            return f"{int(days)} day{'s' if days > 1 else ''} ago"
        elif weeks < 4:
            return f"{int(weeks)} week{'s' if weeks > 1 else ''} ago"
        elif dt.year == now.year:
            return dt.strftime("%b %-d")
        else:
            return dt.strftime("%b %-d, %Y")

