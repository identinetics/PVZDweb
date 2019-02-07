import os
import pathlib
import pytest
assert os.environ["DJANGO_SETTINGS_MODULE"] in ("pvzdweb.settings_pytest_dev", "pvzdweb.settings_pytest"), \
    "require in-memory-db for loading fixtures"

from django.core import management
from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))

from fedop.models import Issuer, Namespaceobj, PolicyStorage, Revocation, Userprivilege

#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def load_tnadmin1():
    management.call_command('migrate')
    tnadmin_data = pathlib.Path('tnadmin/fixtures/tnadmin1.json')
    assert tnadmin_data.is_file(), f'could not find file {tnadmin_data}'
    management.call_command('loaddata', tnadmin_data)

@pytest.fixture(scope="module")
def load_fedop1(load_tnadmin1):
    management.call_command('migrate')
    fedop_data = pathlib.Path('fedop/fixtures/fedop1.json')
    assert fedop_data.is_file(), f'could not find file {fedop_data}'
    management.call_command('loaddata', fedop_data)

def test_issuer(load_fedop1):
    i = Issuer.objects.get(subject_cn='PortalRoot-CA')
    assert i.cacert == "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"
    assert i.pvprole
    assert i.subject_cn

def test_policy_journal():
    assert 1 == len(PolicyJournal.objects.all()), 'PolicyJournal is a singleton, number or records must be equal 1'

def test_revocation():
    r = Revocation.objects.all()[0]  # only one item in testdata
    assert r.subject_cn == '/C=AT/ST=Wien/O=Magistrat der Stadt Wien/OU=MA 14/CN=gondor.magwien.gv.at/emailAddress=cctprod-l@adv.magwien.gv.at'
    assert r.pubkey.startswith('-----BEGIN PUBLIC KEY-----')
    assert r.cert.startswith('MIIFXzCCBEegAwIBAgICAOowDQYJKoZIhvcNAQEFBQAwgZgxC')

def test_namespace():
    n = Namespaceobj.objects.get(fqdn='*.ooe.gv.at')
    assert n.gvouid_parent.gvouid.gvouid == 'AT:L4:000000'
    pass


def test_userprivilege():
    cert = 'MIIEvDCCA6SgAwIBAgIDFioOMA0GCSqGSIb3DQEBBQUAMIGXMQswCQYDVQQGEwJBVDFIMEYGA1UECgw/QS1UcnVzdCBHZXMuIGYuIFNpY2hlcmhlaXRzc3lzdGVtZSBpbSBlbGVrdHIuIERhdGVudmVya2VociBHbWJIMR4wHAYDVQQLDBVhLXNpZ24tUHJlbWl1bS1TaWctMDIxHjAcBgNVBAMMFWEtc2lnbi1QcmVtaXVtLVNpZy0wMjAeFw0xNDExMjUwNzAyMTVaFw0xOTExMjUwNjAyMTVaMGQxCzAJBgNVBAYTAkFUMRkwFwYDVQQDDBBNaWNoYWVsIEbDvHJlZGVyMREwDwYDVQQEDAhGw7xyZWRlcjEQMA4GA1UEKgwHTWljaGFlbDEVMBMGA1UEBRMMMjE1NDc1MjM4NzQxMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEkFtG8MJsanekBz6LMslpeb7u/v4e6liG1jNBU5H/oRR4r4Up4EZThj4i/cdNGOZ9V7BWOg2+9JUYZ80GVCxPWKOCAgwwggIIMBEGA1UdDgQKBAhL88EV5KU2xDAOBgNVHQ8BAf8EBAMCBsAwEwYDVR0jBAwwCoAITd/h/0vZyd8wJQYDVR0RBB4wHIEaTWljaGFlbC5GdWVyZWRlckBvb2UuZ3YuYXQwCQYDVR0TBAIwADB7BggrBgEFBQcBAQRvMG0wQgYIKwYBBQUHMAKGNmh0dHA6Ly93d3cuYS10cnVzdC5hdC9jZXJ0cy9hLXNpZ24tUHJlbWl1bS1TaWctMDJhLmNydDAnBggrBgEFBQcwAYYbaHR0cDovL29jc3AuYS10cnVzdC5hdC9vY3NwMFkGA1UdIARSMFAwRAYGKigAEQELMDowOAYIKwYBBQUHAgEWLGh0dHA6Ly93d3cuYS10cnVzdC5hdC9kb2NzL2NwL2Etc2lnbi1QcmVtaXVtMAgGBgQAizABATAnBggrBgEFBQcBAwEB/wQYMBYwCAYGBACORgEBMAoGCCsGAQUFBwsBMIGaBgNVHR8EgZIwgY8wgYyggYmggYaGgYNsZGFwOi8vbGRhcC5hLXRydXN0LmF0L291PWEtc2lnbi1QcmVtaXVtLVNpZy0wMixvPUEtVHJ1c3QsYz1BVD9jZXJ0aWZpY2F0ZXJldm9jYXRpb25saXN0P2Jhc2U/b2JqZWN0Y2xhc3M9ZWlkQ2VydGlmaWNhdGlvbkF1dGhvcml0eTANBgkqhkiG9w0BAQUFAAOCAQEAvE+Jbdc++ScCq3K/YFrPrc+gDVhtf7EK29m85Y2T7YG/ryPI47ahfin9cenRAB2A9og0slBmgQjJBvv589OaA7JXU6d34k0wiTiv+l/M11jJVD5n8iujIbFLXzRi4nwsFJIOQ9M+5nequBvG803OP9iDsBFn5o9wKMaN9ph0lFixXrpj2m5QQEw6/fKDEh3hu1BRh06neAzaq2KKZ47JERvMyx9MMb/rowdcVzWIZ2SpzxIwKEblhNBG+C0q6fGGvzUwz0Irnf5+KPzrsJpsBr6NDRRKSBJ01nKrB8vBzgAAZSHTd9kMQZA8z9/ZVGSdv8yykV2uxEquIbRfJuvk9Q=='
    u = Userprivilege.objects.get(cert=cert)
    assert u.subject_cn == "Michael Füreder"
    assert u.gvouid_parent.gvouid.gvouid == 'AT:L4:000000'
    pass