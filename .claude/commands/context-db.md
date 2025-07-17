# context-db

Access and search the project's context database (locked requirements, configurations, brand info).

## Usage
```
/context-db list                    # List all context files
/context-db search "brand"          # Search for brand-related context
/context-db load BrandDatabase      # Load specific context
/context-db add-to-prompt brands    # Add to every prompt
```

## What It Does

1. **Discovery** - Helps AI find relevant context files
2. **Loading** - Brings context into current conversation
3. **Auto-Include** - Can add to system prompts
4. **Search** - Find relevant information across all files

## Example Files

### BrandDatabase.json
```json
{
  "Nike": {
    "fullName": "Nike, Inc.",
    "founded": 1964,
    "tagline": "Just Do It",
    "primaryColor": "#111111",
    "allowedInCountries": ["US", "CA", "UK"],
    "tier": "premium",
    "minimumOrderValue": 50
  },
  "Adidas": {
    "fullName": "Adidas AG",
    "founded": 1949,
    "tagline": "Impossible Is Nothing",
    "primaryColor": "#000000",
    "allowedInCountries": ["US", "CA", "UK", "DE"],
    "tier": "premium",
    "minimumOrderValue": 45
  }
}
```

### DatabaseSchema.json
```json
{
  "products": {
    "fields": {
      "id": "uuid PRIMARY KEY",
      "brand": "VARCHAR(50) NOT NULL",
      "name": "VARCHAR(200) NOT NULL",
      "price": "DECIMAL(10,2) NOT NULL",
      "category": "VARCHAR(100)",
      "active": "BOOLEAN DEFAULT true"
    },
    "constraints": [
      "brand must be in approved brands list",
      "price must be > 0",
      "category from enum: footwear, apparel, accessories"
    ]
  }
}
```

## Commands

### List All Context
```bash
/context-db list

CONTEXT DATABASE
================
📁 Requirements (5 files)
  - BrandDatabase.json (5 brands)
  - DatabaseSchema.json (3 tables)
  - CompanyContext.json (company info)
  - ColorPalette.json (design system)
  - APIEndpoints.json (environments)

📌 Anchored Context (3 active)
  - "Use only approved brands"
  - "Database fields are immutable"
  - "Production API only"
```

### Search Context
```bash
/context-db search "Nike"

SEARCH RESULTS for "Nike"
========================
📄 BrandDatabase.json
  - Nike entry found
  - Tier: premium
  - Primary color: #111111
  - Min order: $50

📄 CompanyContext.json
  - Nike partnership details
  - Contract terms
```

### Load Into Conversation
```bash
/context-db load BrandDatabase

✅ Loaded BrandDatabase.json
This context is now available for this conversation.
The AI can now reference:
- 5 brand entries
- Brand-specific colors, taglines
- Tier classifications
- Country restrictions
```

### Auto-Include in Prompts
```bash
/context-db add-to-prompt BrandDatabase

✅ BrandDatabase will be included in every prompt
⚠️  This uses context tokens - use sparingly
```

## Integration with Hooks

When you load context:
1. Drift detector enforces the rules
2. AI has access to the information
3. Changes that violate are blocked

## Best Practices

1. **Organize by Domain**
   ```
   locked/
   ├── brands/
   │   ├── BrandDatabase.json
   │   └── BrandGuidelines.json
   ├── database/
   │   ├── Schema.json
   │   └── Migrations.json
   └── api/
       ├── Endpoints.json
       └── Authentication.json
   ```

2. **Use Descriptive Names**
   - ✅ `BrandDatabase.json`
   - ❌ `data.json`

3. **Include Metadata**
   ```json
   {
     "_metadata": {
       "version": "1.0",
       "lastUpdated": "2024-01-15",
       "description": "Official brand database"
     },
     "brands": { ... }
   }
   ```

4. **Reference in Code**
   ```typescript
   // AI will know to check BrandDatabase.json
   import { BRANDS } from '@/constants/brands';
   // Must match BrandDatabase.json
   ```
