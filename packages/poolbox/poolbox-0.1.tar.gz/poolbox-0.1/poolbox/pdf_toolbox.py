import io
import os
import pdfkit
import re
import subprocess
import sys
import tempfile

from lxml import etree
from jinja2 import Environment, PackageLoader

POOLBOX_TOOLS_PATH = os.getenv('POOLBOX_TOOLS_PATH')


class PDFToolBox(object):
    """."""

    def __init__(self):
        """Check and set necessary tools."""
        self._tools_path = POOLBOX_TOOLS_PATH or ''
        self._tools = self._available_tools()

        # pdftk is mandatory
        if not self._tools[self._tools_path + 'pdftk']:
            raise OSError

    def stamp_pdf(self, pdf_data, stamp_value):
        """Take the pdf, stamp it and return stamped pdf.

        :param pdf_data: binary PDF data
        :param stamp_value: a string to be used as the stamp
        :rtype: stamped binary PDF data
        """
        original_path = self._write(pdf_data)
        stamped_path = tempfile.mkstemp(suffix='.pdf')[1]
        stamp_path = self._write(
            self.render_pdf('stamp.html.j2', {
                'stamp_container_style': 'text-align: right; font-family: arial,sans-serif',
                'stamp_value': stamp_value
            })
        )

        subprocess.call([self._tools_path + 'pdftk', original_path, 'stamp', stamp_path, 'output', stamped_path])

        with open(stamped_path, 'r') as f:
            return f.read()

    def _write(self, data, suffix='.pdf'):
        """Write data in a temporary file and return the path.

        :param data: the data to be written
        :rtype: an absolute path to the file
        """
        path = tempfile.mkstemp(suffix=suffix)[1]
        with open(path, 'w') as f:
            f.write(data)
        return path

    def _available_tools(self):
        """."""
        tools = {}
        for command in (
            self._tools_path + 'pdftk --version',
            self._tools_path + 'wkhtmltopdf --version',
        ):
            try:
                tool = command.split(' ')[0]
                subprocess.call(command.split(' '))
            except OSError:
                print "%s is not available on your environnement." % tool
                tools[tool] = False
            else:
                tools[tool] = True
        return tools

    def render_pdf(self, template, kwargs):
        """Allow you to render PDF based on HTML/J2 template."""
        j2_env = Environment(
            loader=PackageLoader('poolbox', 'templates')
        )
        template = j2_env.get_template(template)
        rendered = template.render(kwargs)
        with io.StringIO(rendered) as html:
            return pdfkit.from_file(html, False)
