# -*- coding: utf-8 -*-

"""."""

import os
import requests
import unittest
import simplejson as json
import subprocess
import tempfile
from base64 import b64encode, b64decode
from poolbox.pdf_toolbox import PDFToolBox


cerfa_fields = {
    "topmostSubform[0].Page1[0].U1A_information[0]": "Oui",
    "topmostSubform[0].Page1[0].D1H_homme[0]": "Oui",
    "topmostSubform[0].Page1[0].D1N_nom[0]": "DUPONT",
    "topmostSubform[0].Page1[0].D1P_prenom[0]": "Gérard",
    "topmostSubform[0].Page1[0].D3N_numero[0]": "86",
    "topmostSubform[0].Page1[0].D3V_voie[0]": "rue St Pierre-lèz-Micquelouceh",
    "topmostSubform[0].Page1[0].D3L_localite[0]": "Marseille",
    "topmostSubform[0].Page1[0].D3C_code[0]": "13011",
    "topmostSubform[0].Page1[0].D3T_telephone[0]": "0625143678",
    "topmostSubform[0].Page1[0].D5A_acceptation[0]": "Oui",
    "topmostSubform[0].Page1[0].D5GE2_email[0]": "gmail.com",
    "topmostSubform[0].Page1[0].D5GE1_email[0]": "jean.dupond"
}


class TestPDFToolBox(unittest.TestCase):
    """."""

    def setUp(self):
        """."""
        self.tool = PDFToolBox()
        pdf_dir = os.path.abspath('./resources')
        self.pdf_data = get_data('%s/cerfa_13410-04_filled.pdf' % pdf_dir)

    def XXXtest_fill_form(self):
        """."""
        pass

    def XXXtest_extract_form_fields(self):
        """."""
        fields = self.tool.extract_form_fields(self.pdf_data)
        self.assertEqual(fields['topmostSubform[0].Page1[0].D1H_homme[0]'], 'Oui')
        self.assertEqual(fields['topmostSubform[0].Page1[0].D1N_nom[0]'], 'DUPONT')
        self.assertEqual(fields['topmostSubform[0].Page1[0].D1P_prenom[0]'], 'G\xc3\xa9rard')

    def test_stamp_pdf(self):
        """."""
        stamp_value = '[For_Your_Eyes_Only]'
        stamped = self.tool.stamp_pdf(self.pdf_data, stamp_value)
        path = tempfile.mkstemp(suffix='.pdf')[1]
        with open(path, 'w') as f:
            f.write(stamped)
        self.assertTrue(pdf_search(path, stamp_value) > 0)


class TestPoolbox(unittest.TestCase):
    """."""

    def setUp(self):
        """."""
        self.base_url = 'http://0.0.0.0:6544'
        pdf_dir = os.path.abspath('./resources')
        self.pdf_b64 = b64encode(get_data('%s/cerfa_13410-04_filled.pdf' % pdf_dir))
        # self.headers = {'content-type': 'application/json'}

    def XXXtest_extract_values(self):
        """."""
        data = json.dumps({
            "base64": self.pdf_b64,
            # "fields": []
        })
        response = requests.post('%s/extract' % self.base_url, data=data)
        fields = response.json()['fields']
        self.assertEqual(fields['topmostSubform[0].Page1[0].D1H_homme[0]'], 'Oui')
        self.assertEqual(fields['topmostSubform[0].Page1[0].D1N_nom[0]'], 'DUPONT')
        self.assertEqual(fields['topmostSubform[0].Page1[0].D1P_prenom[0]'], 'Gérard'.decode('utf-8'))

    def XXXtest_fill_pdf(self):
        """."""
        data = json.dumps({
            "base64": self.pdf_b64,
            "fields": cerfa_fields
        })
        response = requests.post('%s/fill' % self.base_url, data=data)

        self.assertTrue('base64' in response.json())

        pdf = b64decode(response.json()['base64'])
        self.assertTrue(len(pdf) != 0)

    def test_stamp_pdf(self):
        """."""
        stamp_value = '[For_Your_Eyes_Only]'
        data = json.dumps({
            "base64": self.pdf_b64,
            "stamp_value": stamp_value
        })
        response = requests.post('%s/stamp' % self.base_url, data=data)
        self.assertTrue('base64' in response.json())

        pdf = b64decode(response.json()['base64'])
        self.assertTrue(len(pdf) != 0)

        path = tempfile.mkstemp(suffix='.pdf')[1]
        with open(path, 'w') as f:
            f.write(pdf)
        self.assertTrue(pdf_search(path, stamp_value) > 0)


def get_data(path):
    """."""
    with open(path, 'r') as f:
        return f.read()


def pdf_search(pdf_path, query):
    """."""
    text_path = tempfile.mkstemp()[1]
    subprocess.call(['pdftotext', pdf_path, text_path])
    found = 0
    with open(text_path, 'r') as f:
        for line in f.readlines():
            if query in line:
                found += 1
    return found


if __name__ == '__main__':
    unittest.main()
