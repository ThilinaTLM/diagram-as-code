with Diagram("Simple 3-Tier Architecture"):
    users = Users("Users")
    
    with Cluster("Frontend"):
        web = Nginx("Web Server")
    
    with Cluster("Backend"):
        api = EC2("API Server")
    
    with Cluster("Database"):
        db = PostgreSQL("Database")
    
    users >> web >> api >> db