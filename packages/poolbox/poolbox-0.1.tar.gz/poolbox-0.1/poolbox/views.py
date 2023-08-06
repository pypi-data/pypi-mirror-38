""" Cornice services.
"""
from cornice import Service
from pdf_toolbox import PDFToolBox
from base64 import b64decode, b64encode


stamp = Service(name='stamp', path='/stamp', description="Apply a stamp on each PDF page")

stamp_schema = {'base64': str, 'stamp_value': str}


def validator(request, **kwargs):
    """ """
    schema = kwargs['schema']

    if not set(request.json.keys()) == set(schema):
        request.errors.add('body', 'fields', 'Missing or wrong value')
        return

    for key in schema.keys():
        if key == 'base64': 
                try:
                    binary = b64decode(request.json['base64'])
                    if not len(binary):
                        request.errors.add('body', 'base64', 'Empty fields')
                        return
                    request.validated['data'] = binary
                except TypeError:
                    request.errors.add('body', 'base64', 'Not a base64 string')
                    return

        elif key == 'fields':
            # XXX we should check something here
            request.validated['fields'] = request.json['fields']

        else:
            request.validated[key] = request.json[key]


@stamp.post(content_type="application/json", accept="application/json", schema=stamp_schema, validators=(validator,))
def stamp_pdf(request):
    """Take the pdf, stamp it and return stamped pdf.

    Request must provide a JSON object :
    {
        "base64": # binary PDF data encoded in base64,
        "stamp_value": # a string to be used as the stamp
    }

    Response will return a JSON :
    {
        "base64": # stamped binary PDF data encoded in base64
    }
    """
    stamped_pdf = PDFToolBox().stamp_pdf(
        request.validated['data'],
        request.validated['stamp_value']
    )
    return {'base64': b64encode(stamped_pdf)}
