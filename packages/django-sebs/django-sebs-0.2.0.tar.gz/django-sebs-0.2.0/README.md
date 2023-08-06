# django-sebs [![Build Status](https://travis-ci.org/MattBlack85/django-sebs.svg?branch=master)](https://travis-ci.org/MattBlack85/django-sebs)

https://github.com/MattBlack85/django-sebs

Django Simple Email Backend for SES using boto3

## Why another email backend for amazon SES?
That's simple, an EmailBackend must be pluggable, must work out of the box
and must be SIMPLE. 
django-sebs wants to achieve this goal.

## How to use it
Use this email backend is very simple, just override your
EMAIL_BACKEND setting this way:
 - `EMAIL_BACKEND='ses.backend.SESEmailBackend'`

also add 3 additional settings:
 - `SES_ACCESS_KEY='TestKey'` your aws access key
 - `SES_SECRET_KEY='SecretKey'` your aws secret key
 - `SES_REGION='eu-west-1'` the aws region		

## Using DKIM
If you want to use DKIM is enough to enable it in your aws account, that way all emails sent through
the sebs backend will be using the dkim