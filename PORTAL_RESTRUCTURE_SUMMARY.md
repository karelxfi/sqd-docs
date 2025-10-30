# Portal Standalone Product Restructure - Implementation Summary

## Overview

Successfully restructured the SQD documentation to position Portal as a standalone product alongside SDKs, emphasizing Portal as the new blockchain data standard.

## Key Changes Implemented

### 1. Created Portal Documentation Section

**New Directory:** `/en/portal/`

Created comprehensive Portal documentation:

- **`overview.mdx`** - Main Portal landing page emphasizing it as the new blockchain data standard
- **`quickstart.mdx`** - Getting started guide with quick start for Public Portal and Cloud Portal
- **`features.mdx`** - Detailed feature documentation including decentralization, performance, real-time streaming
- **`open-beta.mdx`** - Moved from `/en/network/portal-open-beta.mdx`
- **`self-hosting.mdx`** - Moved from `/en/network/participate/portal.mdx`

**Migration Guides:** `/en/portal/migration/`

- **`from-rpc.mdx`** - New comprehensive guide for migrating from RPC nodes to Portal
- **`cloud-portal-evm.mdx`** - Moved from `/en/cloud/resources/migrate-to-portal-on-evm-or-substrate.mdx`
- **`cloud-portal-solana.mdx`** - Moved from `/en/cloud/resources/migrate-to-portal-on-solana.mdx`

**API Reference:** `/en/portal/api-reference/`

- **`evm.mdx`** - Complete EVM Portal API documentation with examples
- **`solana.mdx`** - Solana Portal API documentation including real-time streaming
- **`substrate.mdx`** - Substrate Portal API documentation

### 2. Updated Home Page (`en/home.mdx`)

- Changed product cards from 3 to 4 columns (`cols={3}` → `cols={4}`)
- Added Portal as the **first** product card (before SDK, Cloud, Network)
- Portal card emphasizes "raw blockchain data through a decentralized network"
- Portal card links to `/en/portal/overview`

### 3. Transformed Choose Your Approach Page (`en/sdk/choose-your-approach.mdx`)

**Before:** Comparison between Pipes SDK and Squid SDK

**After:** Two-tier decision page:

1. **Primary Choice:** Portal vs SDKs (raw data vs processed data)
2. **Secondary Choice:** If SDK chosen, then Pipes vs Squid comparison

Key additions:

- Portal vs SDKs comparison table
- "When to Choose Portal" section
- "When to Choose SDKs" section
- Clear positioning: Portal for raw data, SDKs for transformation/APIs
- Maintained full SDK comparison as subsection

### 4. Updated Navigation (`docs.json`)

**Added Portal Tab:**

- New top-level "Portal" tab after Home tab
- Tagged as "BETA"
- Icon: "network-wired"
- Four main groups:
  - Getting Started (overview, quickstart, features)
  - Access Methods (open-beta, self-hosting)
  - Migration Guides (from-rpc, cloud-portal-evm, cloud-portal-solana)
  - API Reference (evm, solana, substrate)

**Updated Build Tab:**

- Kept existing structure
- Note: Build tab now works alongside Portal tab, emphasizing Portal vs SDK choice

**Updated Cloud Section:**

- Changed migration guide links from `/en/cloud/resources/migrate-to-portal-*` to `/en/portal/migration/cloud-portal-*`

### 5. Updated Internal Links

**Network Catalog Pages (8 files updated):**

- `en/data/catalog/evm/ethereum-mainnet.mdx`
- `en/data/catalog/evm/optimism-mainnet.mdx`
- `en/data/catalog/evm/base-mainnet.mdx`
- `en/data/catalog/evm/arbitrum-one.mdx`
- `en/data/catalog/evm/avalanche-mainnet.mdx`
- `en/data/catalog/evm/abstract-mainnet.mdx`
- `en/data/catalog/evm/polygon-mainnet.mdx`
- `en/data/catalog/evm/zora-mainnet.mdx`

Changed: `/en/cloud/resources/migrate-to-portal/` → `/en/portal/migration/cloud-portal-evm`

**Portal Content Pages:**

- Updated all relative links in `en/portal/open-beta.mdx`
- Updated all relative links in `en/portal/self-hosting.mdx`
- Changed `subsquid-network/` references to `/en/network/`

## Content Strategy

### Portal Positioning

Portal is now positioned as:

- **The new standard for blockchain data**
- **Primary option for raw data access**
- **10-50x faster** than traditional solutions
- **Fully decentralized** with 1,900+ worker nodes
- **Foundation** that SDKs build upon

### SDK Positioning

SDKs are positioned as:

- **Processing layer on top of Portal**
- For developers who need **transformed data**
- For building **applications, APIs, and dApps**
- Choice between streaming (Pipes) or complete framework (Squid)

### Key Messaging

1. **Portal = Raw Data** - Get blockchain data exactly as it exists on-chain
2. **SDKs = Processed Data** - Transform and structure data for applications
3. **Three Access Methods** - Cloud Portal (managed), Self-Hosted (control), Public Portal (free)
4. **Decentralized & Fast** - Network-based architecture delivers superior performance

## Files Created

### Portal Documentation

- `/en/portal/overview.mdx` (NEW)
- `/en/portal/quickstart.mdx` (NEW)
- `/en/portal/features.mdx` (NEW)
- `/en/portal/open-beta.mdx` (MOVED)
- `/en/portal/self-hosting.mdx` (MOVED)

### Migration Guides

- `/en/portal/migration/from-rpc.mdx` (NEW)
- `/en/portal/migration/cloud-portal-evm.mdx` (MOVED)
- `/en/portal/migration/cloud-portal-solana.mdx` (MOVED)

### API Reference

- `/en/portal/api-reference/evm.mdx` (NEW)
- `/en/portal/api-reference/solana.mdx` (NEW)
- `/en/portal/api-reference/substrate.mdx` (NEW)

### Documentation

- `/PORTAL_IMAGE_TODO.md` (Instructions for Portal image creation)
- `/PORTAL_RESTRUCTURE_SUMMARY.md` (This file)

## Files Modified

- `/docs.json` - Added Portal tab, updated Cloud migration links
- `/en/home.mdx` - Added Portal as first product card (4 total)
- `/en/sdk/choose-your-approach.mdx` - Transformed to Portal vs SDK comparison
- `/en/data/catalog/evm/*.mdx` (8 files) - Updated migration guide links

## Outstanding Tasks

### 1. Create Portal Image

**Required:** `/images/PORTAL.png`

This image needs to be created to match the style of existing product images:

- Look at `/images/SDK.png`, `/images/CLOUD.png`, `/images/NETWORK.png` for style reference
- Create gradient background (suggest unique color like teal/cyan or purple)
- Add large white bold "PORTAL" text
- Match dimensions and professional style

**Impact:** Until created, Portal card on home page will show broken image

### 2. Verify Links

All internal links have been updated, but recommended to verify:

- Test all Portal navigation links
- Verify migration guide links from Cloud section
- Check network catalog page links

### 3. Consider Adding

Optional enhancements to consider:

- Portal performance benchmarks page
- Portal use case examples/case studies
- Portal troubleshooting guide
- More detailed Portal vs RPC comparison

## Testing Checklist

- [x] No linting errors in Portal files
- [x] No linting errors in modified files
- [x] All Portal navigation links updated
- [x] All Cloud migration links updated
- [x] All network catalog links updated
- [ ] Portal image created (pending)
- [ ] Test navigation in Mintlify preview
- [ ] Verify all internal links work
- [ ] Test Portal tab navigation
- [ ] Test Build tab navigation

## Key Benefits

1. **Clear Product Positioning** - Portal is now clearly a standalone product
2. **Better User Journey** - Users choose Portal vs SDK based on needs (raw data vs processed)
3. **Improved Discoverability** - Portal has its own top-level tab
4. **Comprehensive Documentation** - Complete Portal docs with quickstart, features, migration, and API reference
5. **Updated Messaging** - Portal positioned as "new blockchain data standard"

## Marketing Impact

- Portal is now **equal** to SDK, Cloud, and Network in navigation hierarchy
- Portal appears **first** in product cards on home page
- Clear value proposition: **10-50x faster**, **fully decentralized**
- Emphasis on Portal as **foundation** that everything else builds on

## Next Steps

1. Create Portal image (`/images/PORTAL.png`)
2. Test all navigation and links in Mintlify preview
3. Consider staging deployment to verify everything works
4. Update any external documentation that references old structure
5. Announce Portal as standalone product to community

## Summary Statistics

- **New Pages Created:** 6
- **Pages Moved:** 5
- **API Reference Pages:** 3
- **Files Modified:** 11
- **Internal Links Updated:** 20+
- **Navigation Groups Added:** 4 (Getting Started, Access Methods, Migration, API Reference)

## Conclusion

Portal is now successfully positioned as a standalone product with comprehensive documentation, clear messaging, and prominent placement in the navigation and home page. The restructure emphasizes Portal as the new blockchain data standard while maintaining clear guidance for users who need SDK-based data processing.
