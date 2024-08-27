import subprocess
import json


def get_partitions(sinfo: json) -> list:
    partition_list = []
    for item in sinfo["sinfo"]:
        if item["port"] == 0:
            continue
        partition_list.append(item["partition"]["name"])
    partition_list = list(set(partition_list))
    return partition_list


def sinfo() -> dict:
    p = subprocess.Popen(["sinfo", "--json"], 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    json_str = out.decode("utf-8")
    sinfo_json = json.loads(json_str)
    partitions = get_partitions(sinfo=sinfo_json)
    return_json = {
        "partitions": partitions,
        "resources": dict()
    }
    for partition in partitions:
        allocated_cpus = 0
        idle_cpus = 0
        total_cpus = 0
        return_json["resources"][partition] = {
            "cpus": {
                "allocated": 0,
                "idle": 0,
                "other": 0,
                "total": 0
            }
        }
    for item in sinfo_json["sinfo"]:
        if item["port"] == 0:
            continue
        partition = item["partition"]["name"]
        if partition.startswith("gpu") or partition.startswith("gpu-"):
            return_json["resources"][partition]['gpus'] = {
                "allocated": 0,
                "idle": 0,
                "other": 0,
                "total": 0
            }
        allocated_cpus = item["cpus"]["allocated"]
        idle_cpus = item["cpus"]["idle"]
        other_cpus = item["cpus"]["other"]
        total_cpus = item["cpus"]["total"]
        return_json["resources"][partition]["cpus"]["allocated"] += allocated_cpus
        return_json["resources"][partition]["cpus"]["idle"] += idle_cpus
        return_json["resources"][partition]["cpus"]["other"] += other_cpus
        return_json["resources"][partition]["cpus"]["total"] += total_cpus
    # return sinfo_json
    return return_json


def main():
    sinfo_json = sinfo()
    with open("sinfo.json", "w") as f:
        json.dump(sinfo_json, f, indent=2)
    print(json.dumps(sinfo_json, indent=2))


if __name__ == "__main__":
    main()
