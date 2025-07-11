import { cn } from '@/lib/utils';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'small' | 'default' | 'large';
}

export function Card({ 
  children, 
  className,
  variant = 'bordered',
  padding = 'default'
}: CardProps) {
  const variants = {
    default: 'bg-white',
    bordered: 'bg-white border border-gray-200',
    elevated: 'bg-white shadow-lg'
  };
  
  const paddings = {
    none: '',
    small: 'p-3',      // 12px
    default: 'p-4',    // 16px
    large: 'p-6'       // 24px
  };
  
  return (
    <div className={cn(
      'rounded-xl',
      variants[variant],
      paddings[padding],
      className
    )}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className }: CardProps) {
  return (
    <div className={cn('space-y-1', className)}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className }: CardProps) {
  return (
    <h3 className={cn(
      'text-size-2 font-semibold text-gray-900',
      className
    )}>
      {children}
    </h3>
  );
}

export function CardDescription({ children, className }: CardProps) {
  return (
    <p className={cn(
      'text-size-3 font-regular text-gray-600',
      className
    )}>
      {children}
    </p>
  );
}

export function CardContent({ children, className }: CardProps) {
  return (
    <div className={cn('text-size-3 font-regular text-gray-700', className)}>
      {children}
    </div>
  );
}

export function CardFooter({ children, className }: CardProps) {
  return (
    <div className={cn('flex items-center gap-3', className)}>
      {children}
    </div>
  );
}
