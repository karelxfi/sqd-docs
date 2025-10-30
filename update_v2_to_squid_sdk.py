#!/usr/bin/env python3
"""
Update all Overview pages to use Squid SDK in V2 Archive tab.
"""

import re
from pathlib import Path

catalog_dir = Path("en/data/catalog/evm")
updated_count = 0

for network_dir in catalog_dir.iterdir():
    if not network_dir.is_dir():
        continue
    
    overview_file = network_dir / "overview.mdx"
    if not overview_file.exists():
        continue
    
    slug = network_dir.name
    
    with open(overview_file, 'r') as f:
        content = f.read()
    
    # Extract network ID from content
    network_id_match = re.search(r'\*\*Network ID\*\*:\s*`([^`]+)`', content)
    if not network_id_match:
        print(f"⚠️  Skipping {slug}: could not find network ID")
        continue
    
    network_id = network_id_match.group(1)
    
    # Find and replace the V2 Archive Usage section
    # Pattern: Find the V2 Archive tab content
    v2_pattern = r'(<Tab title="V2 Archive \(Legacy\)">.*?### Usage\s*\n\s*```typescript[^`]*```\s*\n\s*</Tab>)'
    
    # New Squid SDK usage content
    new_v2_content = f'''<Tab title="V2 Archive (Legacy)">
### V2 Archive Endpoint

```
https://v2.archive.subsquid.io/network/{network_id}
```

<Warning>
  **Legacy**: Rate limited at 50 req/10s per IP. Will be sunset soon.
</Warning>

### Usage

```typescript
import {{ EvmBatchProcessor }} from "@subsquid/evm-processor";

const processor = new EvmBatchProcessor()
  .setGateway("https://v2.archive.subsquid.io/network/{network_id}")
  .setRpcEndpoint("<your_rpc_endpoint>")
  .setFinalityConfirmation(75)
  .setBlockRange({{ from: 0 }});
```

</Tab>'''
    
    # Replace the V2 Archive tab
    new_content = re.sub(v2_pattern, new_v2_content, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(overview_file, 'w') as f:
            f.write(new_content)
        updated_count += 1
        print(f"✓ Updated {slug}")
    else:
        print(f"⚠️  No changes for {slug}")

print(f"\n✓ Updated {updated_count} overview pages with Squid SDK for V2 Archive")

