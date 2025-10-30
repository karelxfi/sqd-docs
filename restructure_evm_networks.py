#!/usr/bin/env python3
"""
Script to restructure all EVM network documentation pages.
Creates Overview and Schema pages for each network.
"""

import os
import re
import json
from pathlib import Path

# Directories
CATALOG_DIR = Path("en/data/catalog/evm")
OUTPUT_BASE = CATALOG_DIR

# Networks already completed
COMPLETED = {"ethereum-mainnet", "arbitrum-one"}

def extract_network_info(content, slug):
    """Extract network information from existing catalog file."""
    info = {
        "network_id": slug,
        "chain_id": "",
        "portal": False,
        "realtime": False,
        "state_diffs": False,
        "traces": False,
        "name": "",
        "description": ""
    }
    
    # Extract title and description from frontmatter
    fm_match = re.search(r'---\s*\ntitle:\s*"([^"]+)"\s*\ndescription:\s*"([^"]+)"', content)
    if fm_match:
        info["name"] = fm_match.group(1)
        info["description"] = fm_match.group(2)
    
    # Extract Network ID
    if match := re.search(r'Network ID[:\s]+`([^`]+)`', content):
        info["network_id"] = match.group(1)
    
    # Extract Chain ID
    if match := re.search(r'Chain ID[:\s]+`?(\d+)`?', content):
        info["chain_id"] = match.group(1)
    
    # Extract features
    info["portal"] = "Portal Status" in content and "Available" in content
    info["realtime"] = "Real-time Streaming" in content and ("Yes" in content or "⚡" in content)
    info["state_diffs"] = "State Diffs" in content and ("Available" in content or "✓" in content)
    info["traces"] = "Traces" in content and ("Available" in content or "✓" in content)
    
    return info

def extract_schema_sections(content):
    """Extract schema sections from existing content."""
    sections = []
    
    # Find all ### headings after "Available Data"
    if "## Available Data" in content:
        data_section = content.split("## Available Data", 1)[1]
        # Split before "## Related Resources" or end
        if "## Related Resources" in data_section:
            data_section = data_section.split("## Related Resources")[0]
        
        # Extract each subsection
        pattern = r'### ([^\n]+)\n\n(\|[^\n]+\n\|[^\n]+\n(?:\|[^\n]+\n)*)'
        matches = re.findall(pattern, data_section, re.MULTILINE)
        
        for title, table in matches:
            sections.append({"title": title.strip(), "table": table.strip()})
    
    return sections

def generate_overview_content(info):
    """Generate overview.mdx content."""
    # Features list
    features = []
    features.append(f'- **Network ID**: `{info["network_id"]}`')
    if info["chain_id"]:
        features.append(f'- **Chain ID**: `{info["chain_id"]}`')
    features.append(f'- **Portal Status**: {"✓ Available" if info["portal"] else "Not Available"}')
    features.append(f'- **Real-time Streaming**: {"⚡ Yes" if info["realtime"] else "Not Available"}')
    features.append(f'- **State Diffs**: {"✓ Available" if info["state_diffs"] else "Not Available"}')
    features.append(f'- **Traces**: {"✓ Available" if info["traces"] else "Not Available"}')
    
    # Generate sample block numbers for examples
    sample_from = 20000000 if "mainnet" in info["network_id"] or info["chain_id"] == "1" else 10000000
    sample_to = sample_from + 1000
    
    # Sample contract address (using common patterns)
    if info["network_id"] == "ethereum-mainnet" or info["chain_id"] == "1":
        sample_address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC on Ethereum
    elif "arbitrum" in info["network_id"]:
        sample_address = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"  # USDC on Arbitrum
    else:
        sample_address = "0x0000000000000000000000000000000000000000"  # Generic example
    
    content = f'''---
title: "Overview"
description: "{info["description"]}"
---

## Network Information

{chr(10).join(features)}

## Endpoints

<Warning>
  V2 archives will be sunset soon. [Migrate to Portal
  →](/en/portal/migration/cloud-portal-evm)
</Warning>

<Tabs>
<Tab title="Portal (Recommended)">
### Portal Endpoint

```
https://portal.sqd.dev/datasets/{info["network_id"]}
```

### Usage

<CodeGroup>
```bash curl
curl -X POST 'https://portal.sqd.dev/datasets/{info["network_id"]}/stream' \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "type": "evm",
    "fromBlock": {sample_from},
    "toBlock": {sample_to},
    "fields": {{
      "block": {{ "number": true, "hash": true }},
      "log": {{ "address": true, "topics": true, "data": true }}
    }},
    "logs": [{{
      "address": ["{sample_address}"]
    }}]
  }}'
```

```typescript TypeScript
import {{ createEvmPortalSource, EvmQueryBuilder }} from "@sqd-pipes/pipes/evm";

const queryBuilder = new EvmQueryBuilder()
  .addFields({{
    block: {{ number: true, hash: true }},
    log: {{ address: true, topics: true, data: true }},
  }})
  .addLog({{
    request: {{ address: ["{sample_address}"] }},
    range: {{ from: {sample_from} }},
  }});

const source = createEvmPortalSource({{
  portal: "https://portal.sqd.dev/datasets/{info["network_id"]}",
  query: queryBuilder,
}});
```

```python Python
import requests

url = "https://portal.sqd.dev/datasets/{info["network_id"]}/stream"
headers = {{"Content-Type": "application/json"}}
payload = {{
    "type": "evm",
    "fromBlock": {sample_from},
    "toBlock": {sample_to},
    "fields": {{
        "block": {{"number": True, "hash": True}},
        "log": {{"address": True, "topics": True, "data": True}}
    }},
    "logs": [{{
        "address": ["{sample_address}"]
    }}]
}}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
```

```go Go
package main

import (
    "bytes"
    "encoding/json"
    "net/http"
)

func main() {{
    url := "https://portal.sqd.dev/datasets/{info["network_id"]}/stream"
    payload := map[string]interface{{}}{{
        "type":      "evm",
        "fromBlock": {sample_from},
        "toBlock":   {sample_to},
        "fields": map[string]interface{{}}{{
            "block": map[string]bool{{"number": true, "hash": true}},
            "log":   map[string]bool{{"address": true, "topics": true, "data": true}},
        }},
        "logs": []map[string]interface{{}}{{
            {{"address": []string{{"{sample_address}"}}}},
        }},
    }}

    jsonData, _ := json.Marshal(payload)
    resp, _ := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
    defer resp.Body.Close()
}}
```
</CodeGroup>

</Tab>

<Tab title="V2 Archive (Legacy)">
### V2 Archive Endpoint

```
https://v2.archive.subsquid.io/network/{info["network_id"]}
```

<Warning>
  **Legacy**: Rate limited at 50 req/10s per IP. Will be sunset soon.
</Warning>

### Usage

```typescript
import {{ EvmBatchProcessor }} from "@subsquid/evm-processor";

const processor = new EvmBatchProcessor()
  .setGateway("https://v2.archive.subsquid.io/network/{info["network_id"]}")
  .setRpcEndpoint("<your_rpc_endpoint>")
  .setFinalityConfirmation(75)
  .setBlockRange({{ from: 0 }});
```

</Tab>
</Tabs>

## Quick Start

Get started indexing {info["name"]} data in minutes:

<CardGroup cols={{2}}>
  <Card
    title="Pipes SDK Quickstart"
    icon="bars-staggered"
    href="/en/sdk/pipes-sdk/quickstart"
  >
    Build a high-performance indexer with the Pipes SDK
  </Card>
  <Card
    title="Squid SDK Quickstart"
    icon="server"
    href="/en/sdk/squid-sdk/evm/quickstart"
  >
    Create a full-stack indexer with GraphQL API
  </Card>
</CardGroup>

## Schema Reference

<Card
  title="View Schema"
  icon="database"
  href="/en/data/catalog/evm/{info["network_id"]}/schema"
>
  See complete field definitions for blocks, transactions, logs{", traces" if info["traces"] else ""}{", and state diffs" if info["state_diffs"] else ""}
</Card>

## Related Resources

<CardGroup cols={{3}}>
  <Card title="EVM API Reference" icon="code" href="/api/evm/dataset-metadata">
    Complete API documentation
  </Card>
  <Card
    title="Migration Guide"
    icon="arrow-right"
    href="/en/portal/migration/cloud-portal-evm"
  >
    Migrate from v2 archives to Portal
  </Card>
  <Card title="Portal Overview" icon="network-wired" href="/en/portal/overview">
    Learn about Portal infrastructure
  </Card>
</CardGroup>
'''
    return content

def generate_schema_content(info, sections):
    """Generate schema.mdx content."""
    description_map = {
        "Blocks": "Block headers contain metadata about each block in the chain.",
        "Transactions": "Transaction data includes all executed transactions with their execution details.",
        "Logs": "Event logs emitted by smart contracts during transaction execution.",
        "Traces": "Internal transactions and call traces showing execution flow within transactions.",
        "State Diffs": "State changes tracking modifications to account balances, storage, and code."
    }
    
    # Build accordion sections
    accordion_content = []
    for section in sections:
        title = section["title"]
        table = section["table"]
        desc = description_map.get(title, f"Data fields for {title.lower()}.")
        
        accordion_content.append(f'''<Accordion title="{title}">
{desc}

{table}
</Accordion>
''')
    
    accordions = "\n".join(accordion_content)
    
    content = f'''---
title: "Schema"
description: "Complete data schema and field reference for {info["name"]}"
---

# {info["name"]} Data Schema

{info["name"]} datasets provide comprehensive on-chain data including blocks, transactions, and logs (events){", traces (internal transactions)" if info["traces"] else ""}{", and state changes" if info["state_diffs"] else ""}. All data is indexed and queryable through Portal or v2 archives.

## Available Data Types

<AccordionGroup>
{accordions}
</AccordionGroup>

## Usage Examples

For code examples showing how to query this data, see:

- [Query Logs Example](/en/sdk/portal-evm/examples/query-logs)
- [Query Transactions Example](/en/sdk/portal-evm/examples/query-transactions)
{"- [Query Traces Example](/en/sdk/portal-evm/examples/query-traces)" if info["traces"] else ""}
{"- [State Diffs Example](/en/sdk/portal-evm/examples/state-diffs)" if info["state_diffs"] else ""}
'''
    return content

def process_network(slug):
    """Process a single network."""
    if slug in COMPLETED:
        print(f"Skipping {slug} (already completed)")
        return None
    
    # Read existing file
    existing_file = CATALOG_DIR / f"{slug}.mdx"
    if not existing_file.exists():
        print(f"Warning: {existing_file} not found")
        return None
    
    with open(existing_file, 'r') as f:
        content = f.read()
    
    # Extract information
    info = extract_network_info(content, slug)
    sections = extract_schema_sections(content)
    
    if not info["name"]:
        print(f"Warning: Could not extract name for {slug}")
        return None
    
    # Create directory
    network_dir = CATALOG_DIR / slug
    network_dir.mkdir(exist_ok=True)
    
    # Generate and write overview
    overview_content = generate_overview_content(info)
    with open(network_dir / "overview.mdx", 'w') as f:
        f.write(overview_content)
    
    # Generate and write schema
    schema_content = generate_schema_content(info, sections)
    with open(network_dir / "schema.mdx", 'w') as f:
        f.write(schema_content)
    
    print(f"✓ Processed {slug} ({info['name']})")
    return {"slug": slug, "name": info["name"]}

def main():
    """Main execution."""
    print("Starting EVM network restructure...")
    print(f"Found {len(list(CATALOG_DIR.glob('*.mdx')))} existing catalog files")
    
    # Get all network slugs
    slugs = [f.stem for f in CATALOG_DIR.glob("*.mdx")]
    processed = []
    
    for slug in sorted(slugs):
        result = process_network(slug)
        if result:
            processed.append(result)
    
    print(f"\nProcessed {len(processed)} networks")
    print(f"Skipped {len(COMPLETED)} already completed networks")
    
    # Save processed list for navigation update
    with open("processed_networks.json", 'w') as f:
        json.dump(processed, f, indent=2)
    
    print("\nNext steps:")
    print("1. Update docs.json navigation")
    print("2. Update evm.mdx View → links")

if __name__ == "__main__":
    main()

