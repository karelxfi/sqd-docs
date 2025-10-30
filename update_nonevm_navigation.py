#!/usr/bin/env python3
"""
Update docs.json navigation for non-EVM networks with nested Overview/Schema structure.
"""

import json

# Network mapping
NETWORKS = {
    "fuel/fuel-mainnet": "Fuel Mainnet",
    "fuel/fuel-testnet": "Fuel Testnet",
    "tron/tron-mainnet": "Tron Mainnet",
    "starknet/starknet-mainnet": "Starknet Mainnet",
    "starknet/starknet-sepolia": "Starknet Sepolia",
    "substrate/acala": "Acala",
    "substrate/astar": "Astar",
    "substrate/kusama": "Kusama",
    "substrate/moonbeam": "Moonbeam",
    "substrate/polkadot": "Polkadot",
    "solana/eclipse-mainnet": "Eclipse Mainnet",
    "solana/solana-mainnet": "Solana Mainnet",
    "solana/soon-mainnet": "Soon Mainnet"
}

# Read docs.json
with open('docs.json', 'r') as f:
    docs = json.load(f)

updated_count = 0

# Find and update non-EVM network sections
for lang in docs['navigation']['languages']:
    if lang['language'] == 'en':
        for tab in lang['tabs']:
            if tab.get('tab') == 'Data Catalog':
                for dropdown in tab.get('dropdowns', []):
                    dropdown_name = dropdown.get('dropdown', '')
                    
                    # Handle Substrate Data
                    if dropdown_name == 'Substrate Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Networks':
                                new_pages = []
                                for page in group['pages']:
                                    if isinstance(page, str) and '/catalog/substrate/' in page:
                                        slug = page.split('/catalog/substrate/')[-1]
                                        network_key = f"substrate/{slug}"
                                        if network_key in NETWORKS:
                                            new_pages.append({
                                                "group": NETWORKS[network_key],
                                                "pages": [
                                                    f"en/data/catalog/substrate/{slug}/overview",
                                                    f"en/data/catalog/substrate/{slug}/schema"
                                                ]
                                            })
                                            updated_count += 1
                                            print(f"✓ Updated {network_key}")
                                        else:
                                            new_pages.append(page)
                                    else:
                                        new_pages.append(page)
                                group['pages'] = new_pages
                    
                    # Handle Solana Data
                    elif dropdown_name == 'Solana Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Networks':
                                new_pages = []
                                for page in group['pages']:
                                    if isinstance(page, str) and '/catalog/solana/' in page:
                                        slug = page.split('/catalog/solana/')[-1]
                                        network_key = f"solana/{slug}"
                                        if network_key in NETWORKS:
                                            new_pages.append({
                                                "group": NETWORKS[network_key],
                                                "pages": [
                                                    f"en/data/catalog/solana/{slug}/overview",
                                                    f"en/data/catalog/solana/{slug}/schema"
                                                ]
                                            })
                                            updated_count += 1
                                            print(f"✓ Updated {network_key}")
                                        else:
                                            new_pages.append(page)
                                    else:
                                        new_pages.append(page)
                                group['pages'] = new_pages
                    
                    # Handle Other Chains dropdown
                    elif dropdown_name == 'Other Chains':
                        for group in dropdown['groups']:
                            # Fuel group
                            if group['group'] == 'Fuel':
                                new_pages = [group['pages'][0]]  # Keep overview page
                                for page in group['pages'][1:]:
                                    if isinstance(page, str) and '/catalog/fuel/' in page:
                                        slug = page.split('/catalog/fuel/')[-1]
                                        network_key = f"fuel/{slug}"
                                        if network_key in NETWORKS:
                                            new_pages.append({
                                                "group": NETWORKS[network_key],
                                                "pages": [
                                                    f"en/data/catalog/fuel/{slug}/overview",
                                                    f"en/data/catalog/fuel/{slug}/schema"
                                                ]
                                            })
                                            updated_count += 1
                                            print(f"✓ Updated {network_key}")
                                        else:
                                            new_pages.append(page)
                                    else:
                                        new_pages.append(page)
                                group['pages'] = new_pages
                            
                            # Tron group
                            elif group['group'] == 'Tron':
                                new_pages = [group['pages'][0]]  # Keep overview page
                                for page in group['pages'][1:]:
                                    if isinstance(page, str) and '/catalog/tron/' in page:
                                        slug = page.split('/catalog/tron/')[-1]
                                        network_key = f"tron/{slug}"
                                        if network_key in NETWORKS:
                                            new_pages.append({
                                                "group": NETWORKS[network_key],
                                                "pages": [
                                                    f"en/data/catalog/tron/{slug}/overview",
                                                    f"en/data/catalog/tron/{slug}/schema"
                                                ]
                                            })
                                            updated_count += 1
                                            print(f"✓ Updated {network_key}")
                                        else:
                                            new_pages.append(page)
                                    else:
                                        new_pages.append(page)
                                group['pages'] = new_pages
                            
                            # Starknet group
                            elif group['group'] == 'Starknet':
                                new_pages = [group['pages'][0]]  # Keep overview page
                                for page in group['pages'][1:]:
                                    if isinstance(page, str) and '/catalog/starknet/' in page:
                                        slug = page.split('/catalog/starknet/')[-1]
                                        network_key = f"starknet/{slug}"
                                        if network_key in NETWORKS:
                                            new_pages.append({
                                                "group": NETWORKS[network_key],
                                                "pages": [
                                                    f"en/data/catalog/starknet/{slug}/overview",
                                                    f"en/data/catalog/starknet/{slug}/schema"
                                                ]
                                            })
                                            updated_count += 1
                                            print(f"✓ Updated {network_key}")
                                        else:
                                            new_pages.append(page)
                                    else:
                                        new_pages.append(page)
                                group['pages'] = new_pages

# Write back
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print(f"\n✓ Updated {updated_count} non-EVM networks in docs.json")

