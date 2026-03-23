import certstream
import json
import datetime

OUTPUT_FILE = "data/ct_logs/ct_stream.jsonl"

def callback(message, context):
    if message["message_type"] == "certificate_update":
        domains = message["data"]["leaf_cert"]["all_domains"]
        entry = {
            "timestamp": str(datetime.datetime.utcnow()),
            "domains": domains
        }
        with open(OUTPUT_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        for d in domains:
            print(f"[+] {d}")

certstream.listen_for_events(callback, url="wss://certstream.calidog.io/")