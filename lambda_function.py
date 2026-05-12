from mangum import Mangum
from upload_image_project.asgi import application #Change to wsgi if needed or if any error occurs

handler = Mangum(application, api_gateway_base_path="/prod", lifespan="off")