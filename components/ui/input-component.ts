import { forwardRef } from 'react';
import { AlertCircle, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  success?: boolean;
  helper?: string;
  icon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, success, helper, icon, className, id, ...props }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    
    return (
      <div className="space-y-2">
        {label && (
          <label 
            htmlFor={inputId} 
            className="text-size-3 font-semibold text-gray-700 block"
          >
            {label}
          </label>
        )}
        
        <div className="relative">
          {icon && (
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
              {icon}
            </div>
          )}
          
          <input
            ref={ref}
            id={inputId}
            className={cn(
              'w-full h-12 px-4 text-size-3 font-regular',
              'border-2 rounded-xl transition-colors',
              'focus:outline-none',
              icon && 'pl-11',
              error && 'border-red-300 focus:border-red-500',
              success && 'border-green-300 focus:border-green-500',
              !error && !success && 'border-gray-200 focus:border-blue-500',
              className
            )}
            {...props}
          />
          
          {(error || success) && (
            <div className="absolute right-4 top-1/2 -translate-y-1/2">
              {error && <AlertCircle className="w-5 h-5 text-red-500" />}
              {success && <Check className="w-5 h-5 text-green-500" />}
            </div>
          )}
        </div>
        
        {(error || helper) && (
          <p className={cn(
            'text-size-4 font-regular',
            error ? 'text-red-600' : 'text-gray-500'
          )}>
            {error || helper}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
