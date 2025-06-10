from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamoDB
from diagrams.aws.management import CloudWatch

with Diagram("Serverless Web Application"):
    users = Users("Users")
    
    with Cluster("Frontend"):
        cdn = CloudFront("CloudFront CDN")
        s3_web = S3("Static Website")
    
    with Cluster("API Layer"):
        api_gateway = APIGateway("API Gateway")
        lambda_auth = Lambda("Auth Function")
        lambda_api = Lambda("API Function")
    
    with Cluster("Data Layer"):
        dynamodb = DynamoDB("DynamoDB")
        s3_data = S3("Data Storage")
    
    with Cluster("Monitoring"):
        cloudwatch = CloudWatch("CloudWatch")
    
    users >> cdn >> s3_web
    users >> api_gateway
    api_gateway >> lambda_auth
    api_gateway >> lambda_api
    lambda_api >> dynamodb
    lambda_api >> s3_data
    [lambda_auth, lambda_api] >> cloudwatch 