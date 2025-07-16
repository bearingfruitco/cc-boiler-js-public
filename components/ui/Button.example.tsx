/**
 * @component Button
 * @used-by AuthForm, ProfileForm, SettingsForm, ContactForm
 * @depends-on cn, Icon
 * @last-scan 2025-01-17
 */

import { cn } from '@/lib/utils';
import { Icon } from './Icon';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  icon?: string;
  className?: string;
}

export function Button({ 
  children, 
  variant = 'primary',
  onClick,
  disabled,
  loading,
  icon,
  className = ''
}: ButtonProps) {
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-800 text-white hover:bg-gray-900'
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={cn(
        'h-12 px-4 rounded-xl font-semibold text-size-3 transition-all',
        'disabled:bg-gray-200 disabled:text-gray-400',
        variants[variant],
        loading && 'cursor-wait',
        className
      )}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <Icon name="spinner" className="animate-spin" />
          Loading...
        </span>
      ) : (
        <span className="flex items-center gap-2">
          {icon && <Icon name={icon} />}
          {children}
        </span>
      )}
    </button>
  );
}
