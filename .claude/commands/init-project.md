# Init Project

Initialize a new project from templates with complete setup.

## Arguments:
- $TEMPLATE: saas-dashboard|marketing-site|e-commerce|internal-tool|custom
- $NAME: Project name

## Why This Command:
- Quick project scaffolding
- Best practices built-in
- Complete setup in minutes
- Consistent structure

## Steps:

### List Templates
```bash
/init-project list

## 📋 Available Templates

### 🏢 SaaS Dashboard
Multi-tenant SaaS with user management
- Auth flow with Supabase
- Dashboard with charts
- Billing integration
- User management
- Analytics

### 🎯 Marketing Site
High-converting landing pages
- Hero sections
- Feature grids
- Testimonials
- Blog with CMS
- Contact forms

### 🛍️ E-commerce
Online store with cart
- Product catalog
- Shopping cart
- Checkout flow
- Order management
- Inventory tracking

### 🔧 Internal Tool
Admin dashboard for teams
- Role-based access
- Data tables
- Reports
- Audit logs
- Integrations

### ✨ Custom
Start from scratch with guidance
```

### Initialize Template
```bash
/init-project saas-dashboard "MyApp"

echo "## 🚀 Initializing SaaS Dashboard: MyApp"
echo ""

# 1. Load template
TEMPLATE=$(cat .claude/templates/saas-dashboard.json)
NAME="MyApp"

# 2. Create structure
echo "### 📁 Creating project structure..."
for dir in $(echo $TEMPLATE | jq -r '.structure.directories[]'); do
  mkdir -p $dir
  echo "✅ Created $dir"
done

# 3. Install dependencies
echo -e "\n### 📦 Installing dependencies..."
DEPS=$(echo $TEMPLATE | jq -r '.dependencies.required[]' | tr '\n' ' ')
pnpm add $DEPS

# Optional deps
echo -e "\n### 📦 Optional dependencies available:"
echo $TEMPLATE | jq -r '.dependencies.optional[]'

# 4. Create components
echo -e "\n### 🎨 Creating initial components..."
for comp in $(echo $TEMPLATE | jq -c '.structure.components[]'); do
  TYPE=$(echo $comp | jq -r '.type')
  NAME=$(echo $comp | jq -r '.name')
  
  echo "Creating $TYPE component: $NAME"
  /create-component $TYPE $NAME --with-tests
done

# 5. Setup environment
echo -e "\n### 🔐 Setting up environment..."
cat > .env.local << EOL
# Required for SaaS Dashboard
$(echo $TEMPLATE | jq -r '.environment.required[]' | sed 's/^/# /' | sed 's/$/ =/')

# Optional
$(echo $TEMPLATE | jq -r '.environment.optional[]' | sed 's/^/# /' | sed 's/$/ =/')
EOL

echo "✅ Created .env.local - Please fill in values"

# 6. Run setup commands
echo -e "\n### 🛠️ Running setup steps..."
STEPS=$(echo $TEMPLATE | jq -c '.setup[]')
for step in $STEPS; do
  DESC=$(echo $step | jq -r '.step')
  echo -e "\n#### $DESC"
  
  CMDS=$(echo $step | jq -r '.commands[]')
  for cmd in $CMDS; do
    echo "Running: $cmd"
    eval "/$cmd"
  done
done

# 7. Apply design system
echo -e "\n### 🎨 Applying design system..."
PRIMARY=$(echo $TEMPLATE | jq -r '.designSystem.primaryColor')
STYLE=$(echo $TEMPLATE | jq -r '.designSystem.style')

# Update tailwind config
cat >> tailwind.config.js << EOL

// Template: SaaS Dashboard
theme: {
  extend: {
    colors: {
      primary: colors.$PRIMARY,
    }
  }
}
EOL

# 8. Create initial context
echo -e "\n### 📝 Creating initial context..."
cat > .claude/context/current.md << EOL
# Project Context - $NAME

## Template: SaaS Dashboard
## Created: $(date +%Y-%m-%d)
## Status: Initial setup complete

### Features Included
$(echo $TEMPLATE | jq -r '.features[]' | sed 's/^/- /')

### Next Steps
1. Fill in environment variables in .env.local
2. Set up Supabase project
3. Configure Stripe webhooks
4. Customize components for your brand

### Quick Commands
- \`/sr\` - See current status
- \`/cc\` - Create new components
- \`/fw start <issue>\` - Start a feature
EOL

# 9. Initialize git
echo -e "\n### 🔧 Initializing git..."
git init
git add .
git commit -m "Initial commit: $NAME from SaaS Dashboard template"

# 10. Final summary
echo -e "\n## ✅ Project Initialized!"
echo ""
echo "### 📊 Summary"
echo "- Template: SaaS Dashboard"
echo "- Components: $(ls components/**/*.tsx | wc -l) created"
echo "- Structure: ✅ Complete"
echo "- Dependencies: ✅ Installed"
echo "- Git: ✅ Initialized"
echo ""
echo "### 🎯 Next Steps"
echo "1. Fill in .env.local with your keys"
echo "2. Run \`pnpm dev\` to start development"
echo "3. Visit http://localhost:3000"
echo ""
echo "### 📚 Documentation"
echo "- Template guide: .claude/templates/saas-dashboard.md"
echo "- Component docs: Run \`/generate-docs\`"
echo "- Commands: Run \`/help\`"
```

### Custom Template
For starting from scratch:

```bash
/init-project custom "MyApp"

## 🎯 Custom Project Setup Wizard

What type of application?
1. Web Application
2. Mobile Web App
3. Admin Dashboard
4. API Service
5. Other

> 1

What features do you need? (space to select)
[ ] Authentication
[x] User profiles
[x] File uploads
[ ] Payments
[x] Search
[ ] Real-time updates
[ ] Analytics

What's your primary use case?
> Internal tool for managing content

## 📋 Recommended Setup

Based on your selections:
- Auth: Supabase (simpler for internal)
- Storage: Supabase Storage
- Search: PostgreSQL full-text
- UI: Dashboard layout

Proceed? (Y/n) > Y

[Continues with customized setup...]
```

### Template Development
Add your own templates:

```bash
/init-project create-template

## 🏗️ Template Creator

Template name: > Customer Portal
Description: > Self-service customer portal
Primary features: > account, orders, support, docs

[Interactive template builder...]

✅ Template saved to .claude/templates/customer-portal.json
```

## Benefits:

1. **Fast Setup** - Complete project in minutes
2. **Best Practices** - Built-in from start
3. **Consistent** - Same structure every time
4. **Customizable** - Easy to modify templates
5. **Documented** - Full setup instructions

This completes the scaffolding for any project type!
