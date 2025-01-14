from rest_framework.throttling import UserRateThrottle
    
class EMAILOTPRateThrottle(UserRateThrottle):
    scope = 'email_otp'
    