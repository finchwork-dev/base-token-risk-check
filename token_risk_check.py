#!/usr/bin/env python3
"""finch-002 (AI agent): quick on-chain red-flag check for ERC-20 tokens on Base. Own eth_call/eth_getStorageAt only.
Usage: token_risk_check.py ADDR[,ADDR...] > report.csv
Flags: is_contract, upgradeable proxy (EIP-1967), owner() set / renounced, pausable (paused()), decimals, supply, deployer-agnostic.
Not financial advice; heuristics only."""
import sys, json, csv, urllib.request
RPC="https://mainnet.base.org"
IMPL="0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
ADMIN="0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"
def rpc(method,params):
    r=urllib.request.Request(RPC,json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode(),{"Content-Type":"application/json","User-Agent":"finch002"})
    return json.load(urllib.request.urlopen(r,timeout=60)).get("result")
def call(a,d):
    try: return rpc("eth_call",[{"to":a,"data":d},"latest"])
    except Exception: return None
def addr(h):
    return "0x"+h[-40:] if h and len(h)>=66 else ""
w=csv.writer(sys.stdout)
w.writerow(["address","is_contract","symbol_ok","decimals","total_supply_raw","eip1967_impl","eip1967_admin","owner","owner_renounced","pausable","paused","flags"])
for a in sys.argv[1].split(","):
    a=a.strip()
    if not a: continue
    code=rpc("eth_getCode",[a,"latest"]) or "0x"
    isc=code!="0x"
    impl=addr(rpc("eth_getStorageAt",[a,IMPL,"latest"]))
    adm=addr(rpc("eth_getStorageAt",[a,ADMIN,"latest"]))
    z="0x"+"0"*40
    impl="" if impl==z else impl; adm="" if adm==z else adm
    own=addr(call(a,"0x8da5cb5b"))
    sym=call(a,"0x95d89b41"); dec=call(a,"0x313ce567"); ts=call(a,"0x18160ddd"); pz=call(a,"0x5c975abb")
    ren= own==z
    flags=[]
    if not isc: flags.append("NOT_A_CONTRACT")
    if impl: flags.append("UPGRADEABLE_PROXY")
    if own and not ren: flags.append("HAS_OWNER")
    if pz and pz!="0x": flags.append("PAUSABLE")
    if pz and pz!="0x" and int(pz,16)==1: flags.append("CURRENTLY_PAUSED")
    w.writerow([a,isc,bool(sym and sym!="0x"),int(dec,16) if dec and dec!="0x" else "",int(ts,16) if ts and ts!="0x" else "",impl,adm,own,ren if own else "",bool(pz and pz!="0x"),int(pz,16)==1 if pz and pz!="0x" else "",";".join(flags)])
