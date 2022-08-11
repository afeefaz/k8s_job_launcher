from sre_constants import SUCCESS
from flask import Flask, request
import json
from job_runner.main import *

import sys
import logging
import json_log_formatter

# logger configurations
formatter = json_log_formatter.JSONFormatter()

streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(formatter)

logger = logging.getLogger('main_logger')
logger.addHandler(streamHandler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <h1>K8s job launcher</h1>
    <h3><a href="/ns">Current Namespace</a></h3>
    <h3><a href="/list_pods">List pods</a></h3>
    <h3><a href="/list_crons">List cron jobs</a></h3>
    <h3><a href="/list_jobs">List jobs</a></h3>
    <h3><a href="/trigger_cron">trigger job manually</a></h3>
    """

@app.route("/ns")
def get_cur_ns():
    ns = get_current_namespace()
    logger.info("The current namespace is : " + ns)

    return ns

@app.route("/list_pods")
def get_pods_list():
    pods = list_pods()
    jsonString = json.dumps(pods, indent=4, default=str)
    
    names = []

    for pod in pods['items']:
        names.append(pod['metadata']['name'])

    js = {
        "msg_content" : "successfuly listed pods",
        "pods_count" : len(pods['items']),
        "pods_names" : names,
        "namespace" : job['metadata']['namespace']
    }
    logger.info(js)

    return jsonString

@app.route("/list_crons")
def list_crons():
    crons = list_cronjobs()
    jsonString = json.dumps(crons, indent=4, default=str)

    names = []

    for cron in crons['items']:
        names.append(cron['metadata']['name'])

    js = {
        "msg_content" : "successfuly listed cron jobs",
        "cronjobs_count" : len(crons['items']),
        "cronjob_names" : names,
        "namespace" : job['metadata']['namespace']
    }
    logger.info(js)

    return jsonString

@app.route("/list_jobs")
def get_jobs_list():
    jobs = list_jobs()
    jsonString = json.dumps(jobs, indent=4, default=str)

    names = []

    for job in jobs['items']:
        names.append(job['metadata']['name'])

    js = {
        "msg_content" : "successfuly listed jobs",
        "jobs_count" : len(jobs['items']),
        "jobs_names" : names,
        "namespace" : job['metadata']['namespace']
    }
    logger.info(js)

    return jsonString

@app.route("/trigger_cron")
def trigger_cron():
    cronjob = request.args.get('cronjob')

    job = create_manual_job(cronjobname=cronjob)
    jsonString = json.dumps(job, indent=4, default=str)

    js = {
        "msg_content" : "successfuly triggered job",
        "job_name" : job['metadata']['name'],
        "cron_job_name" : cronjob,
        "namespace" : job['metadata']['namespace']
        }
    logger.info(js)

    return jsonString

def start_flask_server():
    app.run(port=80, host="0.0.0.0")

if __name__ == '__main__':
   start_flask_server()