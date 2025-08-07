from diagrams import Cluster, Diagram
from diagrams.aws.network import Route53, CloudFront, APIGateway
from diagrams.aws.security import WAF
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.k8s.storage import PV
from diagrams.k8s.infra import ETCD
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users


with Diagram("Digital Identity", show=False):

    # DNS Layer
    # dns_zones = [Route53("DNS Zones") for _ in range(4)]
    # dns_policy = Route53("DNS Security Policy")

    # Presentation Layer
    with Cluster("VPC"):

        with Cluster("Presentation layer"):
            cloudfront = CloudFront("Amazon CloudFront")
            waf = WAF("WAF Policy")
            api_gateway = APIGateway("Amazon API Gateway")
        
        with Cluster("Kubernets: Application Layer"):
            
            # kube = ETCD("K8S")

            with Cluster("Namespace: Wallet services", direction="TB"):
                ingres = Ingress("Ingress")
                wallet = Pod("Wallet service")
                capp = Pod("cApp Service")
                user = Pod("User service")
                cert_vol = PV("Volume") 
            
            with Cluster("Namespace: Verifier services"):
                verifier = Pod("Verifier service")

            with Cluster("Namespace: Issuer services"):
                issuer = Pod("Issuer service")
            
            with Cluster("Namespace: Trusted services"):
                trust_agent = Pod("Trust agent")
                trusted_mail_service = Pod("Trusted notification service")
            
            with Cluster("Namespace: External Services"):
                notification_service = Pod("Notification service")
        
        with Cluster("Database Layer"):
            db = PostgreSQL("Amazon RDS")
            blockchain = Server("HyperLedger Fabric")  # placeholder

    api_gateway >> ingres
    ingres >> capp
    wallet >> issuer
    wallet >> verifier
    notification_service >> trust_agent
    cert_vol >> notification_service
