with Diagram("Microservices Architecture"):
    users = Users("Users")
    
    with Cluster("Load Balancer"):
        lb = ALB("Application Load Balancer")
    
    with Cluster("API Gateway"):
        gateway = APIGateway("API Gateway")
    
    with Cluster("Microservices"):
        user_service = ECS("User Service")
        order_service = ECS("Order Service")
        payment_service = ECS("Payment Service")
    
    with Cluster("Databases"):
        user_db = RDS("User DB")
        order_db = RDS("Order DB")
        payment_db = RDS("Payment DB")
    
    with Cluster("Cache"):
        cache = ElastiCache("Redis Cache")
    
    users >> lb >> gateway
    gateway >> [user_service, order_service, payment_service]
    user_service >> user_db
    order_service >> order_db
    payment_service >> payment_db
    [user_service, order_service] >> cache 