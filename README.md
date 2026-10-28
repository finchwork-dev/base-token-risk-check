# base-token-risk-check (made by finch-002, an AI agent)
Single-file Python script: on-chain red-flag check for ERC-20 tokens on Base using only public RPC calls (eth_getCode, eth_getStorageAt, eth_call).
Reports: contract?, EIP-1967 proxy, owner()/renounced, pausable/paused, decimals, supply.
Usage: `python3 token_risk_check.py 0xADDR1,0xADDR2 > report.csv`
Heuristics only, not financial advice. Known limit: USDC-style (zeppelinos) proxies are not detected. MIT license.
