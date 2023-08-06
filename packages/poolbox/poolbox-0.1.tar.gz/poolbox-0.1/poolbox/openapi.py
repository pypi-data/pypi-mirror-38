from cornice import Service
from cornice.service import get_services
from cornice_swagger import CorniceSwagger

# Create a service to serve our OpenAPI spec
swagger = Service(name='OpenAPI',
                  path='/__api__',
                  description="OpenAPI documentation",
                  cors_origins=('*',),
                  cors_max_age=3600
                  )


@swagger.get()
def openAPI_spec(request):
    doc = CorniceSwagger(get_services())
    doc.summary_docstrings = True
    return doc.generate('pollbox API', '0.1.0')
