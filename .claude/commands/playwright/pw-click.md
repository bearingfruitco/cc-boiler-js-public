# Quick Browser Click Test

Test element clickability without writing code.

## Usage
```bash
/pw-click <selector> [options]

Options:
  --wait       Wait for element (default: 5s)
  --force      Force click even if not visible
  --position   Click position: center|topLeft|topRight|bottomLeft|bottomRight
  --count      Number of clicks (default: 1)
  --delay      Delay between clicks in ms
```

## Examples

```bash
# Test button click
/pw-click "button.submit-btn"

# Click with wait
/pw-click "#dynamic-button" --wait 10

# Double click
/pw-click ".item" --count 2

# Force click hidden element
/pw-click ".dropdown-item" --force

# Click at specific position
/pw-click ".card" --position topRight
```

## What It Does

1. Navigates to current page/component
2. Waits for element to be clickable
3. Performs click action
4. Reports what happened:
   - Success/failure
   - Navigation changes
   - Console errors
   - Visual changes

## Common Use Cases

- Test if buttons work
- Verify dropdown menus
- Check modal triggers
- Test navigation links
- Debug click handlers

Quick way to test interactions! 🖱️
