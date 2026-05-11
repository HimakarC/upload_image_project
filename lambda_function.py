from mangum import Mangum
from upload_image_project.wsgi import application

handler = Mangum(application)