import os
from kubernetes import client, config
from datetime import datetime

########################## Config From local host ##################################
# config.load_kube_config()
config.load_incluster_config()
####################################################################################

########################## Get current namespace ##################################
def get_current_namespace():
    ns_path = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    if os.path.exists(ns_path):
        with open(ns_path) as f:
            return f.read().strip()
    try:
        _, active_context = config.list_kube_config_contexts()
        return active_context["context"]["namespace"]
    except KeyError:
        return "default"
####################################################################################

NAMESPACE = get_current_namespace()

def create_manual_job(cronjobname):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    job_name = 'manual-'+cronjobname+'-'+str(int(ts))

    batch_v1 = client.BatchV1Api()
    batch_v1beta1 = client.BatchV1beta1Api()

    cron_job = batch_v1beta1.read_namespaced_cron_job(cronjobname, NAMESPACE)

    job = client.V1Job(
        api_version='batch/v1',
        kind='Job',
        metadata=client.models.V1ObjectMeta(
            name=job_name,
            annotations={"cronjob.kubernetes.io/instantiate": "manual"}
        ),
        spec=cron_job.spec.job_template.spec
    )

    result = batch_v1.create_namespaced_job(NAMESPACE, job)
    return result.to_dict()

def list_pods():
    v1 = client.CoreV1Api()
    ret = v1.list_namespaced_pod(namespace=NAMESPACE)

    return ret.to_dict()

def list_cronjobs():
    v1 = client.BatchV1Api()
    ret = v1.list_namespaced_cron_job(namespace=NAMESPACE)

    return ret.to_dict()

def list_jobs():
    v1 = client.BatchV1Api()
    ret = v1.list_namespaced_job(namespace=NAMESPACE)

    return ret.to_dict()