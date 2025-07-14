import { cn } from '@/lib/utils';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  padding?: boolean;
  center?: boolean;
}

export function Container({ 
  children, 
  className,
  maxWidth = 'md',
  padding = true,
  center = true
}: ContainerProps) {
  const maxWidths = {
    xs: 'max-w-xs',    // 320px
    sm: 'max-w-sm',    // 384px
    md: 'max-w-md',    // 448px
    lg: 'max-w-lg',    // 512px
    xl: 'max-w-xl'     // 576px
  };
  
  return (
    <div className={cn(
      maxWidths[maxWidth],
      center && 'mx-auto',
      padding && 'px-4',
      className
    )}>
      {children}
    </div>
  );
}
