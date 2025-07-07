from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.alibabacloud.compute import ECS
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import EKS
from diagrams.generic.os import Windows

graph_attr = {
    "fontsize": "20",
    "bgcolor": "transparent"
}

with Diagram("Pixel Streaming Backend", show=True, direction="LR", filename="infra", outformat="png", graph_attr=graph_attr):
    frontend = Windows("Frontend")

    with Cluster("Alibaba Cloud"):
        ecs_streamer = ECS("Streamers with Streaming Worker")

    with Cluster("AWS"):
        signaling_websocket = APIGateway("Signaling Websocket")
        signaling_rest = APIGateway("Signaling REST API")

        with Cluster("EKS"):
            api = EKS("External API")
            api >> signaling_rest

        websocket_handler = Lambda("Websocket Handler")
        http_handler = Lambda("HTTP Handler")

        dynamo_db = Dynamodb("DynamoDB")

        signaling_websocket >> websocket_handler
        signaling_rest >> http_handler
        frontend >> api
        frontend >> Edge(style="dashed") >> signaling_websocket
        ecs_streamer >> Edge(style="dashed") >> signaling_websocket

        websocket_handler >> dynamo_db
        http_handler >> dynamo_db

    websocket_handler >> ecs_streamer
