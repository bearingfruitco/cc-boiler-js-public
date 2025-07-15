# Dependency Fixes Applied

## Issues Resolved

### 1. Deprecated @types/glob
- **Issue**: `@types/glob@9.0.0` is deprecated because glob now provides its own TypeScript definitions
- **Fix**: Removed `@types/glob` from devDependencies since it's no longer needed

### 2. Deprecated Subdependencies
The following deprecated packages were found in the dependency tree:
- `@esbuild-kit/core-utils@3.3.2`
- `@esbuild-kit/esm-loader@2.6.5`
- `glob@7.2.3`
- `inflight@1.0.6`
- `rimraf@2.7.1`

**Fixes Applied**:
- Added pnpm overrides to force newer versions:
  - `glob`: Updated to `^10.3.0` (latest stable)
  - `rimraf`: Updated to `^5.0.0` (latest stable)
- Removed esbuild-kit overrides as they were causing issues

### 3. Node.js url.parse() Deprecation Warning
- **Issue**: `[DEP0169] DeprecationWarning: url.parse() behavior is not standardized`
- **Note**: This is a warning from Node.js about an internal deprecation. It comes from one of the dependencies using the deprecated `url.parse()` method. This will be resolved as dependencies update their code to use the WHATWG URL API.

## How to Apply These Fixes

Run the fix script:
```bash
./fix-dependencies.sh
```

Or manually:
```bash
# Remove deprecated types
pnpm remove @types/glob

# Clean install with updated overrides
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## Verification

After running the fixes, you should:
1. No longer see the @types/glob deprecation warning
2. Have fewer deprecated subdependency warnings
3. The url.parse() warning may still appear until upstream dependencies update

## Future Maintenance

To prevent similar issues:
1. Regularly update dependencies: `pnpm update`
2. Check for outdated packages: `pnpm outdated`
3. Review deprecation warnings during installs
4. Keep the pnpm overrides section updated for known issues
