with Diagram("Kubernetes Deployment"):
    users = Users("Users")
    
    with Cluster("Kubernetes Cluster"):
        with Cluster("Ingress"):
            ingress = Ingress("Nginx Ingress")
        
        with Cluster("Frontend Pods"):
            frontend_pod1 = Pod("Frontend Pod 1")
            frontend_pod2 = Pod("Frontend Pod 2")
            frontend_svc = Service("Frontend Service")
        
        with Cluster("Backend Pods"):
            backend_pod1 = Pod("Backend Pod 1")
            backend_pod2 = Pod("Backend Pod 2")
            backend_svc = Service("Backend Service")
        
        with Cluster("Database"):
            db_pod = Pod("PostgreSQL Pod")
            db_svc = Service("Database Service")
            pv = PersistentVolume("Persistent Volume")
    
    users >> ingress >> frontend_svc
    frontend_svc >> [frontend_pod1, frontend_pod2]
    [frontend_pod1, frontend_pod2] >> backend_svc
    backend_svc >> [backend_pod1, backend_pod2]
    [backend_pod1, backend_pod2] >> db_svc >> db_pod
    db_pod >> pv 