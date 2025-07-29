#!/bin/bash
# Setup script for environment files

echo "🚀 Setting up environment files..."

# Create environment files if they don't exist
if [ ! -f .env.development ]; then
  echo "Creating .env.development..."
  cp .env.example .env.development
  echo "✅ Created .env.development - Please update with your development values"
fi

if [ ! -f .env.staging ]; then
  echo "Creating .env.staging..."
  cp .env.example .env.staging
  # Update NODE_ENV
  sed -i '' 's/NODE_ENV=development/NODE_ENV=staging/' .env.staging
  echo "✅ Created .env.staging - Please update with your staging values"
fi

if [ ! -f .env.production ]; then
  echo "Creating .env.production..."
  cp .env.example .env.production
  # Update NODE_ENV
  sed -i '' 's/NODE_ENV=development/NODE_ENV=production/' .env.production
  # Clear sensitive defaults
  sed -i '' 's/sk_test_.*/sk_live_YOUR_PRODUCTION_KEY/' .env.production
  echo "✅ Created .env.production - Please update with your production values"
fi

# Create .env.local for current environment
if [ ! -f .env.local ]; then
  echo "Creating .env.local..."
  cp .env.development .env.local
  echo "✅ Created .env.local (copy of .env.development)"
fi

# Create necessary directories
mkdir -p .claude/logs/environments
mkdir -p .claude/deployment
mkdir -p backups

echo "
✅ Environment setup complete!

📁 Files created:
  - .env.development
  - .env.staging  
  - .env.production
  - .env.local

📝 Next steps:
  1. Update each .env file with appropriate values
  2. Set up your Supabase projects for each environment
  3. Configure Vercel environment variables
  4. Run 'npm run env:validate' to check configuration

🔒 Security reminder:
  - Never commit .env files to git
  - Use environment variables in CI/CD
  - Rotate keys regularly
"
