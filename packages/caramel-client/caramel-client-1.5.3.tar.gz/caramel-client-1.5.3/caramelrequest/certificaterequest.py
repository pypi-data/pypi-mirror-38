#! /usr/bin/env python

import distutils.spawn
import hashlib
import logging
import os
import subprocess
import sys
import time
import tempfile
from xml.etree import ElementTree as ET

import requests

OPENSSL_CNF = b"""
# This definition stops the following lines choking if HOME isn't
# defined.
HOME            = .
RANDFILE        = $ENV::HOME/.rnd
####################################################################
[ req ]
default_bits        = 2048
default_md      = sha256
default_keyfile     = privkey.pem
distinguished_name  = req_distinguished_name
attributes      = req_attributes
x509_extensions = v3_req    # The extentions to add to the self signed cert
string_mask = utf8only

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment


[ req_distinguished_name ]
countryName         = Country Name (2 letter code)
countryName_default     = AU
countryName_min         = 2
countryName_max         = 2
stateOrProvinceName     = State or Province Name (full name)
stateOrProvinceName_default = Some-State
localityName            = Locality Name (eg, city)
0.organizationName      = Organization Name (eg, company)
0.organizationName_default  = Internet Widgits Pty Ltd
organizationalUnitName      = Organizational Unit Name (eg, section)
commonName          = Common Name (e.g. server FQDN or YOUR name)
commonName_max          = 64
emailAddress            = Email Address
emailAddress_max        = 64

[ req_attributes ]
challengePassword       = A challenge password
challengePassword_min       = 4
challengePassword_max       = 20
unstructuredName        = An optional company name
"""


class CertificateRequestException(Exception):
    def __init__(self, fmt, *args):
        super().__init__(fmt % args)


class CertificateRequest(object):
    def __init__(self, *, server, client_id):
        self.server = server
        self.client_id = client_id
        self.key_file_name = client_id + '.key'
        self.csr_file_name = client_id + '.csr'
        self.crt_temp_file_name = client_id + '.tmp'
        self.crt_file_name = client_id + '.crt'
        self.ca_cert_file_name = server + '.cacert'

    def perform(self):
        self.assert_openssl_available()
        self.ensure_ca_cert_available()
        self.assert_ca_cert_available()
        self.assert_ca_cert_verifies()
        subject = self.get_subject()
        self.ensure_valid_key_file()
        self.ensure_valid_csr_file(subject)
        self.request_cert_from_server()
        self.assert_temp_cert_verifies()
        self.rename_temp_cert()

    def assert_openssl_available(self):
        path = distutils.spawn.find_executable('openssl')
        if path is None:
            raise CertificateRequestException(
                'Cannot find an openssl executable!'
            )

    def assert_ca_cert_available(self):
        if not os.path.isfile(self.ca_cert_file_name):
            raise CertificateRequestException(
                'CA certificate file %s does not exist!',
                self.ca_cert_file_name
            )

    def ensure_ca_cert_available(self):
        url = 'https://{}/root.crt'.format(self.server)
        if not os.path.isfile(self.ca_cert_file_name):
            logging.info('Attempting to fetch CA cert')
            session = requests.Session()
            session.verify = True
            try:
                res = session.get(url)
                res.raise_for_status()
            except requests.exceptions.SSLError as exc:
                raise CertificateRequestException(
                    "Custom CA server or other SSL error: %s",
                    exc
                )
            except Exception:
                raise CertificateRequestException(
                    "Could not download CA file!"
                )
            else:
                with open(self.ca_cert_file_name, 'wb') as f:
                    f.write(res.content)

    def assert_ca_cert_verifies(self):
        result = call_silent('openssl', 'verify',
                             '-CAfile', self.ca_cert_file_name,
                             self.ca_cert_file_name)
        if 0 != result:
            raise CertificateRequestException(
                'CA cert %s is not valid; bailing', self.ca_cert_file_name
            )

    def assert_temp_cert_verifies(self):
        result = call_silent('openssl', 'verify',
                             '-CAfile', self.ca_cert_file_name,
                             self.crt_temp_file_name)
        if 0 != result:
            raise CertificateRequestException(
                'Our new cert %s is not valid; bailing',
                self.crt_temp_file_name
            )

    def rename_temp_cert(self):
        logging.info(
            'Recieved certificate valid; moving it to %s',
            self.crt_file_name
        )
        os.rename(self.crt_temp_file_name,
                  self.crt_file_name)

    def get_subject(self):
        output = check_output_silent('openssl',
                                     'x509',
                                     '-subject',
                                     '-noout',
                                     '-in', self.ca_cert_file_name)
        state = decode_openssl_utf8(output).strip()
# The below ugly thing is for OpenSSL 1.1, as it is no longer outputting a
# format useful as -subject when you parse the subject
# FIXME: EX-TER-MI-NATE
        state = state.replace("C = ", "/C=")
        state = state.replace(", OU = ", "/OU=")
        state = state.replace(", L = ", "/L=")
        state = state.replace(", O = ", "/O=")
        state = state.replace(", ST = ", "/ST=")
        state = state.replace(", CN = ", "/CN=")
        state = state.strip()
        _, value = state.split('subject=', 1)
        value = value.strip()
        prefix, original_cn = value.split('/CN=')
        if prefix == '/C=SE/OU=Caramel/L=Linköping/O=Modio AB/ST=Östergötland':
            prefix = '/C=SE/ST=Östergötland/L=Linköping/O=Modio AB/OU=Caramel'
        return '{prefix}/CN={cn}'.format(prefix=prefix, cn=self.client_id)

    def ensure_valid_key_file(self):
        have_key = False
        if not os.path.isfile(self.key_file_name):
            logging.info(
                'Key file %s does not exist; generating it',
                self.key_file_name
            )
        elif 0 != call_silent('openssl',
                              'pkey',
                              '-noout',
                              '-in', self.key_file_name):
            logging.info(
                'Key file %s is not valid; regenerating it',
                self.key_file_name
            )
        else:
            logging.info(
                'Key file %s is valid; using it',
                self.key_file_name
            )
            have_key = True
        if not have_key:
            result = call_silent('openssl',
                                 'genrsa',
                                 '-out', self.key_file_name,
                                 '2048')
            if result != 0:
                raise CertificateRequestException(
                    'Failed to generate private key!'
                )
            os.chmod(self.key_file_name, 0o600)

    def ensure_valid_csr_file(self, subject):
        have_csr = False
        if not os.path.isfile(self.csr_file_name):
            logging.info(
                'Certificate signing request file %s does not exist; '
                'generating it',
                self.csr_file_name
            )
        elif 0 != call_silent('openssl',
                              'req',
                              '-noout',
                              '-verify',
                              '-in', self.csr_file_name,
                              '-key', self.key_file_name):
            logging.info(
                'Certificate signing request file %s is not valid; '
                'regenerating it',
                self.csr_file_name
            )
        else:
            logging.info(
                'Certificate signing request file %s is valid; using it',
                self.csr_file_name
            )
            have_csr = True
        if not have_csr:
            with tempfile.NamedTemporaryFile() as cnf:
                cnf.write(OPENSSL_CNF)
                cnf.flush()
                result = call_silent('openssl',
                                     'req',
                                     '-config', cnf.name,
                                     '-sha256',
                                     '-utf8',
                                     '-new',
                                     '-key', self.key_file_name,
                                     '-out', self.csr_file_name,
                                     '-subj', subject)
            if result != 0:
                raise CertificateRequestException(
                    'Failed to create certificate signing request!'
                )

    def request_cert_from_server(self):
        csr, csr_hash = self.get_csr_and_hash()
        url = 'https://{}/{}'.format(self.server, csr_hash)

        session = requests.Session()
        session.verify = self.get_ssl_verify_argument()

        response = session.get(url)
        while True:
            if response.status_code == 404:
                logging.info('CSR not posted; posting it')
                response = session.post(url, csr)
            elif response.status_code == 202 or response.status_code == 304:
                logging.info('CSR not processed yet; waiting ...')
                try:
                    time.sleep(15)
                except KeyboardInterrupt:
                    break
                response = session.get(url)
            elif response.status_code == 200:
                logging.info(
                    'Recieved certificate; saving it to %s',
                    self.crt_temp_file_name
                )
                with open(self.crt_temp_file_name, 'wb') as f:
                    f.write(response.content)
                break
            else:
                logging.error('Request failed: %s', parse(response))
                response.raise_for_status()
                break

    def get_ssl_verify_argument(self):
        if self.is_selfsigned_server():
            return self.ca_cert_file_name
        try:
            self.verify_public_ssl_server()
        except requests.exceptions.SSLError as exc:
            raise CertificateRequestException(
                'Problem connecting to CA server: %s', exc
            ) from exc
        else:
            return True

    def is_selfsigned_server(self):
        url = 'https://{}/'.format(self.server)
        session = requests.Session()
        session.verify = self.ca_cert_file_name
        try:
            session.get(url)
        except requests.exceptions.SSLError:
            return False
        return True

    def verify_public_ssl_server(self):
        url = 'https://{}/'.format(self.server)
        session = requests.Session()
        session.verify = True
        session.get(url)

    def get_csr_and_hash(self):
        with open(self.csr_file_name, 'rb') as f:
            csr = f.read()
        return csr, hashlib.sha256(csr).hexdigest()


def printerr(text):
    sys.stderr.write(text + '\n')


def parse(response):
    try:
        result = response.json()
    except Exception:
        result = parse_html(response)
    return result


def parse_html(response):
    return ''.join((e.text or '') + (e.tail or '')
                   for e in ET.fromstring(response.text).iterfind('body//'))


def decode_openssl_utf8(text):
    # Because OpenSSL 1.1 changed how it escapes characters.
    if b'\\\\' in text:
        raise ValueError("There are double encoded backslashes in the subject."
                         " due to openssl 1.1 we do not know how to parse"
                         " this")
# OpenSSL 1.1 changed the quoting output of UTF-8. This causes headache.
# It went from "ST=\xC3\x96sterg\xC3\xB6tland/"
# To: ST = \C3\96sterg\C3\B6tland,
    hacktext = text
    if b'\\x' not in text:
        hacktext = text.replace(b'\\', b'\\x')

    if hacktext != text:
        logging.warning("OpenSSL 1.1 weird unicode hack in place.")

    return bytes(ord(x) for x in hacktext.decode('unicode_escape')) \
        .decode('utf-8')


def call_silent(*args):
    return subprocess.call(args,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)


def check_output_silent(*args):
    return subprocess.check_output(args, stderr=subprocess.DEVNULL)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s')

    if (len(sys.argv) == 3):
        server = sys.argv[1]
        client_id = sys.argv[2]
    else:
        print('Usage: {} SERVER CLIENTID\n'.format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)

    try:
        CertificateRequest(server=server, client_id=client_id).perform()
    except CertificateRequestException as exc:
        logging.error("%s", exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
