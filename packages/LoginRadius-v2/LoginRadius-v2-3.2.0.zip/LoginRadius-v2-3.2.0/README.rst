LoginRadius offers a complete social infrastructure solution combining 30 major social platforms into one unified API.
With LoginRadius, websites and mobile apps can integrate social login, enable social sharing, capture user profiles and
social data, create a single sign-on experience for their users, and get comprehensive social analytics.
Our social solution helps websites engage, understand, and leverage their users.

This module provides a wrapper for urllib2 or the requests library to easily access the API from
https://docs.loginradius.com/ in a more "pythonic" way. Providing easier access to essential data in a few lines of code.
This will work with 2.0 API specifications.

For more information, visit: http://loginradius.com/

Prerequisites
========

You will need at least Python - 2.7 or greater. LoginRadius module utilizes the namedtuple from the collections library
and the import_module from importlib.

From Package
=========

Using pip

pip install loginradius

or with easy_install

easy_install loginradius

Changelog
======
3.2.0
-----

### Enhancements

-   Updated demo with new UI and features.
-   Unit tests.
-   Bug fixes.
-   New V2 API's:
    -   Auth Privacy Policy Accept
    -   Auth Send Welcome Email
    -   Auth Verify Email by OTP
    -   Auth Delete Account
    -   Account Email Delete
    -   Phone Login Using OTP
    -   Phone Send OTP
    -   Remove Phone ID by Access Token
    -   2FA Validate Google Auth Code
    -   2FA Validate OTP
    -   Validate Backup Code
    -   Update MFA by Access Token
    -   Update MFA Setting
    -   One Touch Verify OTP by Email
    -   Get Active Session Details
    -   Access Token via Vkontakte Token
    -   Access Token via Google Token
    -   Refresh User Profile
    -   Refresh Token
    -   Delete All Records by Datasource

### Breaking Changes

-   Replaced deprecated  [pycrypto package](https://pypi.org/project/pycrypto/)  with  [cryptography package](https://pypi.org/project/cryptography/)  for SOTT generation
-   Updated some existing API's:
    -   Get Roles by UID: moved to role class
    -   Assign Roles by UID: moved role class
    -   One Touch Login: moved to authentication.login class
    -   Get Backup Code by Access Token: moved to authentication.TwoFactor class
    -   Reset Backup Code by Access Token: moved to authentication.TwoFactor class
    -   Get Backup Code by UID: moved to account.TwoFactor class
    -   Reset Backup Code by UID: moved to account.TwoFactor class
	
	
3.0.1
-----

* Added Readme and History file

3.0.0
-----

* Added Latest V2 APIs.