from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class ContactAnonRateThrottle(AnonRateThrottle):
    rate = '1/minute'

class ContactUserRateThrottle(UserRateThrottle):
    rate = '2/minute'