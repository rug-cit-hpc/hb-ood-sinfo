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
    p = subprocess.Popen(["sinfo", "--exact", 
                          "--Format", "NodeList:80,CPUsState,Nodes,AllocMem,Memory,Gres:30,GresUsed:30,PartitionName"], 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return {"error": err.decode("utf-8")}
        sys.exit(1)
    node_types = ["regular", "a100gpu", "v100gpu", "himem", "parallel", "gelifes"]
    return_json = {
        "node_types": node_types,
        "resources": {
            'regular': {
                'cpus': {
                    'allocated': 0,
                    'idle': 0,
                    'other': 0,
                    'total': 0
                }
            },
            'a100gpu': {
                'cpus': {
                    'allocated': 0,
                    'idle': 0,
                    'other': 0,
                    'total': 0
                }
            },
            'v100gpu': {
                'cpus': {
                    'allocated': 0,
                    'idle': 0,
                    'other': 0,
                    'total': 0
                }
            },
            'himem': {
                'cpus': {
                    'allocated': 0,
                    'idle': 0,
                    'other': 0,
                    'total': 0
                }
            },
            'parallel': {
                'cpus': {
                    'allocated': 0,
                    'idle': 0,
                    'other': 0,
                    'total': 0
                }
            },
            'gelifes': {
                'cpus': {
                    'allocated': 0,
                    'idle': 0,
                    'other': 0,
                    'total': 0
                }
            }
        }
    }
    for line in out.decode("utf-8").split("\n"):
        no_fields = len(line.split())
        if no_fields != 8:
            continue
        else:
            node_list, cpu_state, nodes, alloc_mem, mem, gres, gres_used, partition_name = line.split()
            if not partition_name.endswith("short"):
                continue
            if node_list.startswith("node"):
                node_type = "regular"
            elif node_list.startswith("a100gpu"):
                node_type = "a100gpu"
            elif node_list.startswith("v100gpu"):
                node_type = "v100gpu"
            elif node_list.startswith("memory"):
                node_type = "himem"
            elif node_list.startswith("omni"):
                node_type = "parallel"
            elif node_list.startswith("gelifes"):
                node_type = "gelifes"
            allocated_cpus, idle_cpus, other_cpus, total_cpus = cpu_state.split("/")
            return_json["resources"][node_type]["cpus"]["allocated"] += int(allocated_cpus)
            return_json["resources"][node_type]["cpus"]["idle"] += int(idle_cpus)
            return_json["resources"][node_type]["cpus"]["other"] += int(other_cpus)
            return_json["resources"][node_type]["cpus"]["total"] += int(total_cpus)
            # print(allocated_cpus)
    # json_str = out.decode("utf-8")
    # sinfo_json = json.loads(json_str)
    # partitions = get_partitions(sinfo=sinfo_json)
    # for partition in partitions:
    #     allocated_cpus = 0
    #     idle_cpus = 0
    #     total_cpus = 0
    #     return_json["resources"][partition] = {
    #         "cpus": {
    #             "allocated": 0,
    #             "idle": 0,
    #             "other": 0,
    #             "total": 0
    #         },
    #         "memory": {
    #             "allocated": 0,
    #             "idle": 0,
    #             "other": 0,
    #             "total": 0
    #         },
    #     }
    # for item in sinfo_json["sinfo"]:
    #     if item["port"] == 0:
    #         continue
    #     partition = item["partition"]["name"]
    #     if partition.startswith("gpu") or partition.startswith("gpu-"):
    #         return_json["resources"][partition]['gpus'] = {
    #             "allocated": 0,
    #             "idle": 0,
    #             "other": 0,
    #             "total": 0
    #         }
    #     allocated_cpus = item["cpus"]["allocated"]
    #     idle_cpus = item["cpus"]["idle"]
    #     other_cpus = item["cpus"]["other"]
    #     total_cpus = item["cpus"]["total"]
    return return_json


def main():
    sinfo_json = sinfo()
    print(json.dumps(sinfo_json, indent=2))


if __name__ == "__main__":
    main()
