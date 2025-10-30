#!/usr/bin/env python3
"""
Script to restructure all 87 Substrate networks from the table.
Creates Overview and Schema pages for each network.
"""

import os
import re
from pathlib import Path

CATALOG_BASE = Path("en/data/catalog/substrate")

# Generic Substrate schema template
SUBSTRATE_SCHEMA_SECTIONS = [
    {
        "title": "Blocks",
        "description": "Block data contains metadata about each block in the chain.",
        "table": """| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `number` | integer | Block number |
| `hash` | string | Block hash |
| `parent_hash` | string | Parent block hash |
| `timestamp` | integer | Block timestamp |
| `state_root` | string | State root hash |
| `extrinsics_root` | string | Extrinsics root hash |
| `spec_version` | integer | Runtime specification version |"""
    },
    {
        "title": "Extrinsics",
        "description": "Extrinsics (transactions) submitted to the network.",
        "table": """| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `index` | integer | Extrinsic index in block |
| `hash` | string | Extrinsic hash |
| `version` | integer | Extrinsic version |
| `signature` | object | Signature information |
| `success` | boolean | Whether extrinsic succeeded |
| `error` | object | Error information if failed |
| `call` | object | Call data |"""
    },
    {
        "title": "Events",
        "description": "Events emitted during block execution.",
        "table": """| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `index` | integer | Event index |
| `phase` | string | Execution phase (ApplyExtrinsic, Finalization, Initialization) |
| `extrinsic_index` | integer | Associated extrinsic index |
| `name` | string | Event name |
| `args` | object | Event arguments |
| `topics` | array | Event topics |"""
    },
    {
        "title": "Calls",
        "description": "Call data from extrinsic execution.",
        "table": """| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `name` | string | Call name (pallet.method) |
| `args` | object | Call arguments |
| `origin` | object | Call origin |
| `success` | boolean | Whether call succeeded |
| `error` | object | Error information if failed |"""
    }
]

def parse_substrate_networks(file_path):
    """Extract network names and slugs from substrate.mdx table."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    networks = []
    # Match table rows: | Network Name | https://v2.archive.subsquid.io/network/{slug} |
    pattern = r'\|\s*([^|]+?)\s*\|\s*https://v2\.archive\.subsquid\.io/network/([a-z0-9\-]+)\s*\|'
    matches = re.findall(pattern, content)
    
    for name, slug in matches:
        # Clean up network name
        name = name.strip()
        # Remove footnote markers like (*), (**), etc.
        name = re.sub(r'\s*\(\*+\)\s*$', '', name)
        networks.append({
            'name': name,
            'slug': slug
        })
    
    return networks

def generate_overview_content(network_name, network_slug):
    """Generate overview.mdx content for a Substrate network."""
    content = f'''---
title: "Overview"
description: "{network_name} data indexing and API access"
---

<Info>
  Starting today (2025-02-23) all open private network gateways are rate limited
  at 50 requests per 10 seconds per IP. Higher bandwidths will soon become
  available via the public network.
</Info>

## Network Information

- **Network ID**: `{network_slug}`
- **Gateway**: Open Private Network

## Endpoints

### Gateway Endpoint

```
https://v2.archive.subsquid.io/network/{network_slug}
```

### Usage

```typescript
import {{ SubstrateBatchProcessor }} from '@subsquid/substrate-processor'

const processor = new SubstrateBatchProcessor()
  .setGateway("https://v2.archive.subsquid.io/network/{network_slug}")
  .setRpcEndpoint("<your_rpc_endpoint>")
  .setBlockRange({{ from: 0 }});
```

## Quick Start

Get started indexing {network_name} data:

<Card
  title="CLI Cheatsheet"
  icon="terminal"
  href="/en/sdk/squid-sdk/substrate/quickstart"
>
  Quick reference for building your indexer
</Card>

## Schema Reference

<Card
  title="View Schema"
  icon="database"
  href="/en/data/catalog/substrate/{network_slug}/schema"
>
  See complete field definitions for all data types
</Card>

## Related Resources

<CardGroup cols={{2}}>
  <Card title="API Reference" icon="code" href="/en/subsquid-network/reference/substrate-api">
    Complete API documentation
  </Card>
  <Card title="Network Overview" icon="network-wired" href="/en/subsquid-network/overview">
    Learn about the Subsquid Network
  </Card>
</CardGroup>
'''
    return content

def generate_schema_content(network_name):
    """Generate schema.mdx content for a Substrate network."""
    # Build accordion sections
    accordion_content = []
    for section in SUBSTRATE_SCHEMA_SECTIONS:
        accordion_content.append(f'''<Accordion title="{section["title"]}">
{section["description"]}

{section["table"]}
</Accordion>
''')
    
    accordions = "\n".join(accordion_content)
    
    content = f'''---
title: "Schema"
description: "Complete data schema and field reference for {network_name}"
---

# {network_name} Data Schema

{network_name} datasets provide comprehensive on-chain data indexed and queryable through the Subsquid Network.

## Available Data Types

<AccordionGroup>
{accordions}
</AccordionGroup>
'''
    return content

def process_all_substrate_networks():
    """Process all Substrate networks from the table."""
    # Parse the substrate networks file
    substrate_file = Path("en/data/networks/substrate.mdx")
    networks = parse_substrate_networks(substrate_file)
    
    print(f"Found {len(networks)} Substrate networks")
    
    total_created = 0
    total_updated = 0
    
    for network in networks:
        network_name = network['name']
        network_slug = network['slug']
        
        # Create directory
        network_dir = CATALOG_BASE / network_slug
        network_dir.mkdir(parents=True, exist_ok=True)
        
        overview_file = network_dir / "overview.mdx"
        schema_file = network_dir / "schema.mdx"
        
        # Generate and write overview
        overview_content = generate_overview_content(network_name, network_slug)
        with open(overview_file, 'w') as f:
            f.write(overview_content)
        
        # Generate and write schema
        schema_content = generate_schema_content(network_name)
        with open(schema_file, 'w') as f:
            f.write(schema_content)
        
        if overview_file.exists() and schema_file.exists():
            total_created += 1
            print(f"  ✓ {network_slug} ({network_name})")
    
    print(f"\n✓ Processed {total_created} Substrate networks")
    return networks

if __name__ == "__main__":
    print("Starting Substrate network restructure...")
    networks = process_all_substrate_networks()
    print(f"\nCreated {len(networks) * 2} pages ({len(networks)} overview + {len(networks)} schema)")

