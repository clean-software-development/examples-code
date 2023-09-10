from mangum import Mangum
from fastapi_in_aws_lambda.app import app
handler = Mangum(app, lifespan="off")