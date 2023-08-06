# Source: https://github.com/johnwheeler/flask-ask/blob/master/flask_ask/verifier.py
# License: Apache-2.0 https://github.com/johnwheeler/flask-ask/blob/master/LICENSE.txt
# Edited by Tim Woocker (Nov 2018)

import base64
import json
import posixpath
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import urlopen

import aniso8601
from OpenSSL import crypto
from django.conf import settings
from django.http import HttpRequest

from . import VerificationError


def is_valid_request(request: HttpRequest) -> bool:
    url = request.META.get("SignatureCertChainUrl")
    signature = request.META.get("Signature")
    body = json.loads(request.body.decode())
    if not _valid_certificate_url(url):
        return False
    cert_data = urlopen(url).read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
    if not _valid_certificate(cert):
        return False
    if not verify_signature(cert, signature, request.body):
        return False
    if getattr(settings, "DEBUG", False):
        timestamp = _parse_timestamp(body.get('request', {}).get('timestamp'))
        if not verify_timestamp(timestamp):
            return False

    # TODO: Check application id on request
    # try:
    #     application_id = body['session']['application']['applicationId']
    # except KeyError:
    #     application_id = body['context']['System']['application']['applicationId']


def verify_signature(cert, signature, signed_data):
    try:
        signature = base64.b64decode(signature)
        crypto.verify(cert, signature, signed_data, 'sha1')
    except crypto.Error:
        return False
    return True


def verify_timestamp(timestamp) -> bool:
    dt = datetime.utcnow() - timestamp.replace(tzinfo=None)
    return not(abs(dt.total_seconds()) > 150)


def verify_application_id(candidate, records):
    if candidate not in records:
        raise VerificationError("Application ID verification failed")


def _valid_certificate_url(cert_url):
    parsed_url = urlparse(cert_url)
    if parsed_url.scheme == 'https':
        if parsed_url.hostname == "s3.amazonaws.com":
            if posixpath.normpath(parsed_url.path).startswith("/echo.api/"):
                return True
    return False


def _valid_certificate(cert):
    not_after = cert.get_notAfter().decode('utf-8')
    not_after = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
    if datetime.utcnow() >= not_after:
        return False
    found = False
    for i in range(0, cert.get_extension_count()):
        extension = cert.get_extension(i)
        short_name = extension.get_short_name().decode('utf-8')
        value = str(extension)
        if 'subjectAltName' == short_name and 'DNS:echo-api.amazon.com' == value:
            found = True
            break
    if not found:
        return False
    return True


def _parse_timestamp(timestamp):
    """
    Parse a given timestamp value, raising ValueError if None or Flasey
    """
    if timestamp:
        try:
            return aniso8601.parse_datetime(timestamp)
        except AttributeError:
            # raised by aniso8601 if raw_timestamp is not valid string
            # in ISO8601 format
            try:
                return datetime.utcfromtimestamp(timestamp)
            except:
                # relax the timestamp a bit in case it was sent in millis
                return datetime.utcfromtimestamp(timestamp / 1000)

    raise ValueError('Invalid timestamp value! Cannot parse from either ISO8601 string or UTC timestamp.')
