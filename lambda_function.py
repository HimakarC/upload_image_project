from mangum import Mangum
from upload_image_project.asgi import application

handler = Mangum(application)