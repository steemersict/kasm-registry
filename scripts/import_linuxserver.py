#!/usr/bin/env python3
"""Importeert LinuxServer.io-workspaces (schema 1.0, 1.1 voor Chromium/Firefox) als schema 1.1 voor Kasm 1.16-1.19."""
import json, os, re, urllib.request
SRC = "https://kasmregistry.linuxserver.io"
VERS = ["1.16.x", "1.17.x", "1.18.x", "1.19.x"]
get = lambda u: urllib.request.urlopen(u).read()
v10 = json.loads(get(f"{SRC}/1.0/list.json"))["workspaces"]
v11 = {w["friendly_name"]: w for w in json.loads(get(f"{SRC}/1.1/list.json"))["workspaces"]}
os.chdir(os.path.join(os.path.dirname(__file__), "..", "workspaces"))
for w in v10:
    n = w["friendly_name"]
    if n in v11:  # 1.1-bron is leidend
        w = v11[n]
        comp = [{**c, "version": v} for v in VERS for c in [w["compatibility"][-1]]]
    else:
        comp = [{"version": v, "image": w["name"], "uncompressed_size_mb": w["uncompressed_size_mb"]} for v in VERS]
    out = {k: w[k] for k in ("description", "docker_registry", "image_src", "run_config", "exec_config", "categories", "friendly_name", "architecture") if k in w}
    out["compatibility"] = comp
    d = re.sub(r"[^A-Za-z0-9 ._-]", "", n)
    if os.path.exists(f"{d}/workspace.json"): continue  # bv. Ferdium staat al los
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(f"{d}/workspace.json", "w"), indent=2); open(f"{d}/workspace.json", "a").write("\n")
    open(f"{d}/{w['image_src']}", "wb").write(get(f"{SRC}/1.0/icons/{w['image_src']}"))
