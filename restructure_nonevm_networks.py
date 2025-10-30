#!/usr/bin/env python3
"""
Script to restructure all non-EVM network documentation pages.
Creates Overview and Schema pages for Fuel, Tron, Starknet, Substrate, and Solana networks.
"""

import os
import re
from pathlib import Path

# Network configurations
NETWORKS = {
    "fuel": {
        "networks": ["fuel-mainnet", "fuel-testnet"],
        "processor": "FuelDataSource",
        "import": "import { FuelDataSource } from '@subsquid/fuel-stream'",
        "quickstart": "/en/fuel-indexing/cli-cheatsheet",
        "api_ref": "/en/fuel-indexing/network-api/fuel-api"
    },
    "tron": {
        "networks": ["tron-mainnet"],
        "processor": "TronBatchProcessor",
        "import": "import { TronBatchProcessor } from '@subsquid/tron-processor'",
        "quickstart": "/en/tron-indexing/cli-cheatsheet",
        "api_ref": "/en/tron-indexing/network-api/tron-api"
    },
    "starknet": {
        "networks": ["starknet-mainnet", "starknet-sepolia"],
        "processor": "StarknetDataSource",
        "import": "import { StarknetDataSource } from '@subsquid/starknet-stream'",
        "quickstart": "/en/sdk/squid-sdk/starknet/quickstart",
        "api_ref": "/en/subsquid-network/reference/starknet-api"
    },
    "substrate": {
        "networks": ["acala", "astar", "kusama", "moonbeam", "polkadot"],
        "processor": "SubstrateBatchProcessor",
        "import": "import { SubstrateBatchProcessor } from '@subsquid/substrate-processor'",
        "quickstart": "/en/sdk/squid-sdk/substrate/quickstart",
        "api_ref": "/en/subsquid-network/reference/substrate-api"
    },
    "solana": {
        "networks": ["eclipse-mainnet", "solana-mainnet", "soon-mainnet"],
        "processor": "SolanaDataSource",
        "import": "import { SolanaDataSource } from '@subsquid/solana-stream'",
        "quickstart": "/en/solana-indexing/how-to-start/cli-cheatsheet",
        "api_ref": "/en/solana-indexing/network-api/solana-api"
    }
}

CATALOG_BASE = Path("en/data/catalog")

def extract_schema_sections(content):
    """Extract schema sections from existing content."""
    sections = []
    
    if "## Available Data" in content:
        data_section = content.split("## Available Data", 1)[1]
        
        # Extract each subsection
        pattern = r'### ([^\n]+)\n\n(\|[^\n]+\n\|[^\n]+\n(?:\|[^\n]+\n)*)'
        matches = re.findall(pattern, data_section, re.MULTILINE)
        
        for title, table in matches:
            sections.append({"title": title.strip(), "table": table.strip()})
    
    return sections

def get_network_name(content):
    """Extract network name from frontmatter."""
    match = re.search(r'title:\s*"([^"]+)"', content)
    return match.group(1) if match else "Unknown Network"

def generate_overview_content(chain_type, network_id, network_name, config):
    """Generate overview.mdx content."""
    processor = config["processor"]
    import_line = config["import"]
    quickstart = config["quickstart"]
    api_ref = config["api_ref"]
    
    # Chain-specific usage examples
    if chain_type == "fuel":
        usage_example = f'''{import_line}

const dataSource = new FuelDataSource()
  .setGateway("https://v2.archive.subsquid.io/network/{network_id}")
  .setFields({{
    block: {{ height: true }},
    transaction: {{ id: true }},
    receipt: {{ receiptType: true, data: true }}
  }});'''
    
    elif chain_type == "tron":
        usage_example = f'''{import_line}

const processor = new TronBatchProcessor()
  .setGateway("https://v2.archive.subsquid.io/network/{network_id}")
  .setBlockRange({{ from: 0 }});'''
    
    elif chain_type == "starknet":
        usage_example = f'''{import_line}

const dataSource = new StarknetDataSource()
  .setGateway("https://v2.archive.subsquid.io/network/{network_id}")
  .setBlockRange({{ from: 0 }});'''
    
    elif chain_type == "substrate":
        usage_example = f'''{import_line}

const processor = new SubstrateBatchProcessor()
  .setGateway("https://v2.archive.subsquid.io/network/{network_id}")
  .setRpcEndpoint("<your_rpc_endpoint>")
  .setBlockRange({{ from: 0 }});'''
    
    else:  # solana
        usage_example = f'''{import_line}

const dataSource = new SolanaDataSource()
  .setGateway("https://v2.archive.subsquid.io/network/{network_id}")
  .setBlockRange({{ from: 0 }});'''
    
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

- **Network ID**: `{network_id}`
- **Gateway**: Open Private Network

## Endpoints

### Gateway Endpoint

```
https://v2.archive.subsquid.io/network/{network_id}
```

### Usage

```typescript
{usage_example}
```

## Quick Start

Get started indexing {network_name} data:

<Card
  title="CLI Cheatsheet"
  icon="terminal"
  href="{quickstart}"
>
  Quick reference for building your indexer
</Card>

## Schema Reference

<Card
  title="View Schema"
  icon="database"
  href="/en/data/catalog/{chain_type}/{network_id}/schema"
>
  See complete field definitions for all data types
</Card>

## Related Resources

<CardGroup cols={{2}}>
  <Card title="API Reference" icon="code" href="{api_ref}">
    Complete API documentation
  </Card>
  <Card title="Network Overview" icon="network-wired" href="/en/subsquid-network/overview">
    Learn about the Subsquid Network
  </Card>
</CardGroup>
'''
    return content

def generate_schema_content(network_name, chain_type, sections):
    """Generate schema.mdx content."""
    description_map = {
        "Blocks": "Block data contains metadata about each block in the chain.",
        "Transactions": "Transaction data includes all executed transactions with their details.",
        "Logs": "Event logs emitted during transaction execution.",
        "Instructions": "Instructions executed within transactions.",
        "Receipts": "Receipt data from transaction execution.",
        "Inputs": "Transaction inputs.",
        "Outputs": "Transaction outputs.",
        "Account Updates": "Changes to account states.",
        "Events": "Event data emitted by the network.",
        "Extrinsics": "Extrinsics (transactions) submitted to the network.",
        "Calls": "Call data from extrinsic execution.",
        "Contracts": "Smart contract interaction data.",
        "Internal Transactions": "Internal transaction traces.",
        "Messages": "Cross-layer messages.",
        "State Updates": "State change information."
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
    
    accordions = "\n".join(accordion_content) if accordion_content else "<Accordion title=\"Data\">\nNo schema information available.\n</Accordion>"
    
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

def process_all_networks():
    """Process all non-EVM networks."""
    total_processed = 0
    
    for chain_type, config in NETWORKS.items():
        print(f"\nProcessing {chain_type.upper()} networks...")
        chain_dir = CATALOG_BASE / chain_type
        
        for network_id in config["networks"]:
            # Read existing file
            existing_file = chain_dir / f"{network_id}.mdx"
            if not existing_file.exists():
                print(f"  ⚠️  Warning: {existing_file} not found")
                continue
            
            with open(existing_file, 'r') as f:
                content = f.read()
            
            # Extract information
            network_name = get_network_name(content)
            sections = extract_schema_sections(content)
            
            # Create directory
            network_dir = chain_dir / network_id
            network_dir.mkdir(exist_ok=True)
            
            # Generate and write overview
            overview_content = generate_overview_content(chain_type, network_id, network_name, config)
            with open(network_dir / "overview.mdx", 'w') as f:
                f.write(overview_content)
            
            # Generate and write schema
            schema_content = generate_schema_content(network_name, chain_type, sections)
            with open(network_dir / "schema.mdx", 'w') as f:
                f.write(schema_content)
            
            total_processed += 1
            print(f"  ✓ {network_id} ({network_name})")
    
    print(f"\n✓ Processed {total_processed} non-EVM networks")
    return total_processed

if __name__ == "__main__":
    print("Starting non-EVM network restructure...")
    count = process_all_networks()
    print(f"\nCreated {count * 2} new pages ({count} overview + {count} schema)")

