# -*- coding: utf-8 -*-
import logging

import boto3
import botocore
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address

logger = logging.getLogger('sebs')


class SESEmailBackend(BaseEmailBackend):
    """
    A boto3 wrapper around the django mail backend, this allows to
    send your emails through amazon SES.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super(SESEmailBackend, self).__init__(
            fail_silently=fail_silently, **kwargs)
        self.connection = None

    def open(self):
        self.connection = boto3.client(
            'ses',
            aws_access_key_id=settings.SES_ACCESS_KEY,
            aws_secret_access_key=settings.SES_SECRET_KEY,
            region_name=settings.SES_REGION
        )

    def close(self):
        self.connection = None

    def send_messages(self, email_messages):
        self.open()
        num_sent = 0

        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1

        self.close()

        return num_sent

    def _send(self, email_message):
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]
        try:
            self.connection.send_email(
                Source=from_email,
                Destination={'ToAddresses': recipients},
                Message={'Subject': {'Data': email_message.subject,
                                     'Charset': 'utf-8'},
                         'Body': {'Text': {'Data': email_message.body,
                                           'Charset': 'utf-8'},
                                  'Html': {'Data': email_message.body,
                                           'Charset': 'utf-8'}}}
            )
        except botocore.exceptions.ClientError as exc:
            logger.warning('An error occured when trying to send the email via SES: %s' % exc.msg)
            if not self.fail_silently:
                raise
            return False
        return True
