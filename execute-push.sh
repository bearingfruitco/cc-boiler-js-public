#!/bin/bash
# Execute the push operations

cd /Users/shawnsmith/dev/bfc/boilerplate

# Make the script executable
chmod +x push-to-both-repos.sh

# Execute it
./push-to-both-repos.sh

# Clean up the temporary script
rm push-to-both-repos.sh

echo "✅ Push operation completed!"
