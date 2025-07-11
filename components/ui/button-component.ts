import { forwardRef } from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'default' | 'large' | 'small';
  loading?: boolean;
  fullWidth?: boolean;
  icon?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    children, 
    variant = 'primary',
    size = 'default',
    loading = false,
    fullWidth = true,
    icon,
    disabled,
    className,
    ...props
  }, ref) => {
    const baseClasses = 'rounded-xl font-semibold transition-all flex items-center justify-center gap-2 disabled:cursor-not-allowed';
    
    const variants = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-200 disabled:text-gray-400',
      secondary: 'bg-gray-800 text-white hover:bg-gray-900 disabled:bg-gray-200 disabled:text-gray-400',
      ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 disabled:text-gray-400',
      danger: 'bg-red-600 text-white hover:bg-red-700 disabled:bg-gray-200 disabled:text-gray-400'
    };
    
    const sizes = {
      small: 'h-10 px-3 text-size-4',    // 40px - use sparingly
      default: 'h-12 px-4 text-size-3',  // 48px - preferred
      large: 'h-14 px-6 text-size-2'     // 56px - emphasis
    };
    
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          baseClasses,
          variants[variant],
          sizes[size],
          fullWidth && 'w-full',
          className
        )}
        {...props}
      >
        {loading && <Loader2 className="w-4 h-4 animate-spin" />}
        {icon && !loading && icon}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
