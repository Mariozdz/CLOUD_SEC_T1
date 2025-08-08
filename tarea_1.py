from diagrams import Cluster, Diagram, Edge
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

    with Cluster("DNS"):
        dns_zone_1 = Route53("DNS Zone 1")
        dns_zone_2 = Route53("DNS Zone 2")
        dns_zone_3 = Route53("DNS Zone 3")
        #dns_zones = [Route53("DNS Zones") for _ in range(3)]
        dns_policy = Route53("DNS Security Policy")

    with Cluster("Legacy services"):
        legacy_issuer = Server("Legacy Issuer")
        legacy_verifier = Server("Legacy Verifier")
        legacy_issuer - legacy_verifier

    # Presentation Layer
    with Cluster("VPC"):

        with Cluster("Presentation layer"):
            cloudfront = CloudFront("Amazon CloudFront")
            waf = WAF("WAF Policy")
            api_gateway = APIGateway("Amazon API Gateway")
        
        with Cluster("Kubernets: Application Layer"):
            
            # kube = ETCD("K8S")
            ingresController = Ingress("Ingress Controller")

            with Cluster("Namespace: Wallet services", direction="TB"):
                ingress = Ingress("Ingress")

                wallet = Pod("Wallet service")
                capp = Pod("cApp Service")
                cert_vol = PV("Volume") 
            
            with Cluster ("Namespace: User services"):
                user = Pod("User service")
            
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

    # Connections based on edges with transparent color are not valid - related

    issuer >> legacy_issuer
    verifier >> legacy_verifier

    dns_policy >> Edge(color="transparent") >> dns_zone_1
    dns_policy >> Edge(color="transparent") >> dns_zone_2
    dns_policy >> Edge(color="transparent") >> dns_zone_3
    dns_zone_3 >> Edge(color="transparent") >> api_gateway
    api_gateway >> ingresController
    ingresController >> ingress
    ingress >> capp
    capp >> Edge(label="Read blockchain") >> user
    user >> Edge(label="Read") >> blockchain
    cert_vol >> Edge(color="transparent") >> capp
    capp >> verifier
    capp >> wallet
    capp  >> trust_agent
    wallet >> blockchain
    wallet >> issuer
    wallet >> verifier
    # notification_service >> trust_agent
    issuer >> Edge(color="transparent") >> trust_agent
    trusted_mail_service >> Edge(color="transparent") >> notification_service
    notification_service >> Edge(color="transparent") >> db
