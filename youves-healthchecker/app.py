import json
import os

import requests
from flask import Flask

STATE_QUERY = """query {
    dipdup_index {
      level
      name
      config_hash
      created_at
      status
    }
    dipdup_head {
    name
    level
    created_at
  }
}"""
TZKT_URL = os.getenv("TZKT_URL", "https://api.tzkt.io")
HEALTH_DELTA = int(os.getenv("HEALTH_DELTA", 40))


def do_probe(only_realtime=True):
    # get latest block
    try:
        r = requests.get(TZKT_URL + "/v1/blocks?sort.desc=level&limit=1")
        latest_block = json.loads(r.text)[0]["level"]
        # get sync state
        url = "http://localhost:8080/v1/graphql"
        r = requests.post(url, json={"query": STATE_QUERY})

        sync_level = latest_block
        delta = 0

        for k in json.loads(r.text)["data"]["dipdup_head"]:
            sync_level = min(sync_level, k["level"])
        delta = latest_block - sync_level
    except Exception as e:
        print("EXCEPTION")
        print(r)
        print(r.text)
        print("e")
        print(e)
        return {"ok": False, "msg": "could not get graphql"}, 400

    if delta > HEALTH_DELTA:
        return {"ok": False, "delta": delta}, 400

    for k in json.loads(r.text)["data"]["dipdup_index"]:
        if (only_realtime and k["status"] != "REALTIME") or not k["status"] in [
            "REALTIME",
            "SYNCING",
        ]:
            return {"ok": False, "not_ready_index": k["name"]}, 400

    return {"ok": True, "delta": delta}


app = Flask(__name__)


@app.route("/health")
def checker_health():
    return {"ok": True}


@app.route("/startup")
def normal_startup_probe():
    return do_probe()


@app.route("/liveness")
def liveness_probe():
    return do_probe(False)
