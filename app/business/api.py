import logging
import os
from nameko.standalone.rpc import ServiceRpcProxy, ClusterRpcProxy

config = {"AMQP_URI": os.getenv("RMQ", 'amqp://guest:guest@localhost/')}


def rpc_proxy(service_name: str):
    logging.info(f"RPC {service_name} called")
    return ServiceRpcProxy({service_name}, config)


def rpc_request(user_credentials: str, service_rpc: str, action: str):
    try:
        with ClusterRpcProxy(config) as rpc:
            service = getattr(rpc, service_rpc)
            method = getattr(service, "start_task")
            method({"user_credentials": user_credentials, "action": action})
    except Exception as e:
        return {
            "message": f"Serviço {service_rpc}->start_task esta temporariamente indisponível, tente mais tarde. "
                       f"Except = {e}"
        }
    return True
