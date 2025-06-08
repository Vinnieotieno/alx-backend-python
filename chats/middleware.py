import logging
from datetime import datetime, time, timedelta
from collections import defaultdict

from django.http import HttpResponseForbidden, JsonResponse


logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(message)s")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Not known"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Define restricted hours of access
        self.allowed_start = time(18, 0)  # 6:00 PM
        self.allowed_end = time(21, 0)  # 9:00 PM

    def __call__(self, request):
        current_time = datetime.now().time()
        if not (self.allowed_start <= current_time <= self.allowed_end):
            return HttpResponseForbidden("Access allowed between 6-9 PM")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = defaultdict(list)
        self.message_limit = 5
        self.time_window = timedelta(minutes=1)

    def get_client_ip(self, request):
        """Helper method to get the clinet IP even if behing proxy"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clear up old timestamps
            timestamps = self.ip_message_log[ip]
            timestamps = [t for t in timestamps if now - t < self.time_window]
            self.ip_message_log[ip] = timestamps

            # Check if limit is exceeded
            if len(timestamps) >= self.message_limit:
                return JsonResponse(
                    {"err": "You have exceeded message limit rate. Jaribu baadye"},
                    status=429,  # Too many requests
                )
            self.ip_message_log[ip].append(now)

        return self.get_response(request)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            # Allow admins or moderators only
            if (
                not user.is_superuser
                or user.groups.filter(name__in=["moderator"]).exists()
            ):
                return HttpResponseForbidden(
                    "Access denied: Admin or Moderator privileges requred"
                )
        return self.get_response(request)