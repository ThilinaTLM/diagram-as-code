from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.aws.compute import EC2
from diagrams.onprem.database import PostgreSQL

with Diagram("Simple 3-Tier Architecture"):
    users = Users("Users")
    
    with Cluster("Frontend"):
        web = Nginx("Web Server")
    
    with Cluster("Backend"):
        api = EC2("API Server")
    
    with Cluster("Database"):
        db = PostgreSQL("Database")
    
    users >> web >> api >> db