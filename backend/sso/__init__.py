"""
The Authentication for KISA
----------------------------
Goals:
- Integration with KAIST SSO
- Security and usability
- Don't reinvent the wheel too much

Implementation:
- KAIST SSO Integration and differnt run levels with 2nd factor authentication (TOTP)
    - The 2nd factor is to give additional security in addition to KAIST SSO (especially for website adminstration)
    - There are two run levels 
        - normal django login (can be checked via `user.is_authenticated`)
        - otp verified (can checked via `user.is_verified(request)`)
    - TOTP
        - change TOTP secret (requires otp verification)
        - forgot TOTP secret (requires SSO login + mail verification)
        - change mail (requires otp verification)
    - How to login 
        - like any other `POST` requests these requests will require CSRF token in the header
        - for SSO login
            - send a `POST` request to /sso/login with or without 'next'(the url to be redirected after login)
            - check the response; if redirect follow else do error-handling
        - for 2nd factor OTP
            - send a `POST` request including the otp to /sso/check_totp
        - for logout
            - send a `POST` request to /sso/logout
            - check the response; if redirect follow else do error-handling

Configuration:
- gmail-api-token.json in the root of backend folder
- `utils.GMailAPI.get_api_token()` will help you reissue the api token; it must be run outside the container

Testing:
- `tests.login()` will help you with the login

"""
TOTP_SESSION_KEY = '_totp_verified'