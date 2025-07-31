# Component Patterns

> Best practices and examples for building components with Claude Code Boilerplate

## 📚 Table of Contents

- [Basic Component Pattern](#basic-component-pattern)
- [Form Components](#form-components)
- [Data Display Components](#data-display-components)
- [Interactive Components](#interactive-components)
- [Composite Components](#composite-components)
- [Design System Compliance](#design-system-compliance)

---

## 🎯 Basic Component Pattern

### The Foundation

Every component follows this structure:

```typescript
// components/ui/Button.tsx
import { type VariantProps, cva } from "class-variance-authority"
import { forwardRef } from "react"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  // Base styles - using design system
  "inline-flex items-center justify-center rounded-md text-size-4 font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-11 px-4 py-2",      // 44px - minimum touch target
        sm: "h-9 rounded-md px-3",
        lg: "h-12 rounded-md px-8",      // 48px - preferred touch target
        icon: "h-11 w-11",               // Square touch target
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

### Creating with Command

```bash
# Basic component
/cc Button

# With variants
/cc Button --variants=primary,secondary,destructive --sizes=sm,md,lg

# With tests
/cc Button --with-tests

# Complete package
/cc Button --complete
# Creates:
# - Component
# - Tests
# - Stories
# - Documentation
```

---

## 📝 Form Components

### Secure Form Pattern

```bash
# Create tracked form with security
/ctf ContactForm --vertical=debt --compliance=tcpa
```

Generated component:

```typescript
// components/forms/ContactForm.tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useEventTracking } from "@/hooks/use-event-tracking"
import { encryptField } from "@/lib/security/encryption"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

// Type-safe schema from field registry
const formSchema = z.object({
  firstName: z.string().min(2, "First name required"),
  lastName: z.string().min(2, "Last name required"),
  email: z.string().email("Valid email required"),
  phone: z.string().regex(/^\d{10}$/, "10-digit phone required"),
  consent: z.boolean().refine((val) => val === true, {
    message: "Consent required for TCPA compliance",
  }),
})

type FormData = z.infer<typeof formSchema>

export function ContactForm() {
  const { trackEvent } = useEventTracking()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      phone: "",
      consent: false,
    },
  })

  async function onSubmit(values: FormData) {
    setIsSubmitting(true)
    
    try {
      // Encrypt PII fields
      const encryptedData = {
        ...values,
        email: await encryptField(values.email, "email"),
        phone: await encryptField(values.phone, "phone"),
      }

      // Non-blocking event tracking
      trackEvent({
        action: "form_submitted",
        category: "contact",
        label: "debt_vertical",
        metadata: {
          form_id: "contact-form",
          has_consent: values.consent,
        },
      })

      // Submit to API
      await submitContactForm(encryptedData)

      // Success handling
      form.reset()
      toast.success("Thank you! We'll contact you soon.")
    } catch (error) {
      // Error tracking
      trackEvent({
        action: "form_error",
        category: "contact",
        error: error.message,
      })
      
      toast.error("Something went wrong. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Form {...form}>
      <form 
        onSubmit={form.handleSubmit(onSubmit)} 
        className="space-y-6"
        data-testid="contact-form"
      >
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="firstName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>First Name</FormLabel>
                <FormControl>
                  <Input 
                    placeholder="John" 
                    {...field} 
                    data-pii="true"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name="lastName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Last Name</FormLabel>
                <FormControl>
                  <Input 
                    placeholder="Doe" 
                    {...field}
                    data-pii="true" 
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input 
                  type="email"
                  placeholder="john@example.com" 
                  {...field}
                  data-pii="true"
                  autoComplete="email"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="phone"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Phone</FormLabel>
              <FormControl>
                <Input 
                  type="tel"
                  placeholder="(555) 123-4567" 
                  {...field}
                  data-pii="true"
                  autoComplete="tel"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="consent"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0">
              <FormControl>
                <Checkbox
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>
                  I consent to receive calls and texts at the number provided
                </FormLabel>
                <FormMessage />
              </div>
            </FormItem>
          )}
        />

        <Button 
          type="submit" 
          disabled={isSubmitting}
          className="w-full"
        >
          {isSubmitting ? "Submitting..." : "Submit"}
        </Button>
      </form>
    </Form>
  )
}
```

### Key Patterns

1. **PII Protection**: Fields marked with `data-pii="true"`
2. **Encryption**: Sensitive fields encrypted before submission
3. **Event Tracking**: Non-blocking, privacy-compliant
4. **TCPA Compliance**: Explicit consent required
5. **Error Handling**: User-friendly with tracking

---

## 📊 Data Display Components

### Table Pattern

```bash
# Create data table
/cc UserTable --type=data-table
```

```typescript
// components/tables/UserTable.tsx
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

interface User {
  id: string
  name: string
  email: string
  role: string
  status: "active" | "inactive"
}

const columns: ColumnDef<User>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => (
      <div className="font-semibold text-size-4">
        {row.getValue("name")}
      </div>
    ),
  },
  {
    accessorKey: "email",
    header: "Email",
    cell: ({ row }) => (
      <div className="text-size-4 text-muted-foreground">
        {row.getValue("email")}
      </div>
    ),
  },
  {
    accessorKey: "role",
    header: "Role",
    cell: ({ row }) => (
      <Badge variant="outline">{row.getValue("role")}</Badge>
    ),
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string
      return (
        <Badge 
          variant={status === "active" ? "success" : "secondary"}
        >
          {status}
        </Badge>
      )
    },
  },
]

export function UserTable({ data }: { data: User[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <TableHead key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(
                      cell.column.columnDef.cell,
                      cell.getContext()
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell
                colSpan={columns.length}
                className="h-24 text-center"
              >
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  )
}
```

---

## 🎮 Interactive Components

### Modal Pattern

```bash
# Create modal
/cc ConfirmationModal --type=dialog
```

```typescript
// components/modals/ConfirmationModal.tsx
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"

interface ConfirmationModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onConfirm: () => void
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  destructive?: boolean
}

export function ConfirmationModal({
  open,
  onOpenChange,
  onConfirm,
  title,
  description,
  confirmText = "Confirm",
  cancelText = "Cancel",
  destructive = false,
}: ConfirmationModalProps) {
  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          <AlertDialogDescription className="text-size-4">
            {description}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>{cancelText}</AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            className={destructive ? "bg-destructive text-destructive-foreground" : ""}
          >
            {confirmText}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
```

---

## 🔗 Composite Components

### Card with Actions Pattern

```bash
# Create composite component
/cc ProductCard --composite
```

```typescript
// components/cards/ProductCard.tsx
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { formatCurrency } from "@/lib/utils"

interface ProductCardProps {
  product: {
    id: string
    name: string
    description: string
    price: number
    category: string
    inStock: boolean
    image: string
  }
  onAddToCart: (id: string) => void
  onViewDetails: (id: string) => void
}

export function ProductCard({ 
  product, 
  onAddToCart, 
  onViewDetails 
}: ProductCardProps) {
  return (
    <Card className="overflow-hidden">
      <div className="aspect-square relative">
        <img
          src={product.image}
          alt={product.name}
          className="object-cover w-full h-full"
        />
        {!product.inStock && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <Badge variant="secondary" className="text-size-3">
              Out of Stock
            </Badge>
          </div>
        )}
      </div>
      
      <CardHeader className="space-y-2">
        <div className="flex items-start justify-between">
          <h3 className="text-size-3 font-semibold line-clamp-1">
            {product.name}
          </h3>
          <Badge variant="outline" className="text-size-4">
            {product.category}
          </Badge>
        </div>
        <p className="text-size-4 text-muted-foreground line-clamp-2">
          {product.description}
        </p>
      </CardHeader>
      
      <CardContent>
        <p className="text-size-2 font-semibold">
          {formatCurrency(product.price)}
        </p>
      </CardContent>
      
      <CardFooter className="gap-2">
        <Button
          variant="default"
          size="sm"
          onClick={() => onAddToCart(product.id)}
          disabled={!product.inStock}
          className="flex-1"
        >
          Add to Cart
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onViewDetails(product.id)}
        >
          Details
        </Button>
      </CardFooter>
    </Card>
  )
}
```

---

## ✅ Design System Compliance

### Validation Commands

```bash
# Check single component
/vd components/ui/Button.tsx

# Check all components
/validate-design

# Auto-fix violations
/vd --fix
```

### Common Violations and Fixes

#### ❌ Wrong Font Size
```typescript
// Bad
<p className="text-sm">Small text</p>
<h1 className="text-4xl">Big heading</h1>

// Good
<p className="text-size-4">Small text</p>
<h1 className="text-size-1">Big heading</h1>
```

#### ❌ Wrong Font Weight
```typescript
// Bad
<span className="font-bold">Bold text</span>
<span className="font-medium">Medium text</span>

// Good
<span className="font-semibold">Semibold text</span>
<span className="font-regular">Regular text</span>
```

#### ❌ Non-Grid Spacing
```typescript
// Bad
<div className="p-5">Content</div>
<div className="mt-7">Content</div>

// Good
<div className="p-6">Content</div>     // 24px (6 * 4)
<div className="mt-8">Content</div>    // 32px (8 * 4)
```

#### ❌ Small Touch Targets
```typescript
// Bad
<button className="h-8 w-8">X</button>

// Good
<button className="h-11 w-11">X</button>  // 44px minimum
```

---

## 🎨 Component Creation Workflow

### 1. Plan with PRP
```bash
/create-prp user-avatar-component
```

### 2. Generate with Validation
```bash
/cc UserAvatar --from-prp
```

### 3. Test Immediately
```bash
/tr UserAvatar.test.tsx
```

### 4. Check Design Compliance
```bash
/vd components/ui/UserAvatar.tsx
```

### 5. Document Usage
```bash
/doc-component UserAvatar
```

---

## 📚 Additional Resources

- [Testing Component Patterns](../testing/component-testing.md)
- [Accessibility Guidelines](../design/accessibility.md)
- [Performance Optimization](../development/performance.md)
- [Component Library Reference](../features/COMPONENT_LIBRARY.md)

---

**Remember**: Every component should be accessible, performant, and strictly follow the design system. The boilerplate's validation ensures this happens automatically!
