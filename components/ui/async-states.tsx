/**
 * Async state components following design system rules
 * Used for loading, error, and empty states in async operations
 */

import { Loader2, AlertTriangle, Inbox } from 'lucide-react';
import { Button } from './button-component';

interface LoadingStateProps {
  message?: string;
  size?: 'small' | 'default' | 'large';
}

export function LoadingState({ 
  message = 'Loading...', 
  size = 'default' 
}: LoadingStateProps) {
  const sizeClasses = {
    small: 'w-4 h-4',
    default: 'w-8 h-8',
    large: 'w-12 h-12'
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <Loader2 className={`animate-spin text-blue-600 ${sizeClasses[size]}`} />
      {message && (
        <p className="text-size-3 text-gray-600 text-center">{message}</p>
      )}
    </div>
  );
}

interface ErrorStateProps {
  error: Error | { message: string };
  retry?: () => void;
  compact?: boolean;
}

export function ErrorState({ error, retry, compact = false }: ErrorStateProps) {
  const errorMessage = error instanceof Error ? error.message : error.message;

  if (compact) {
    return (
      <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-xl">
        <AlertTriangle className="w-4 h-4 text-red-600 shrink-0" />
        <p className="text-size-4 text-red-700 flex-1">{errorMessage}</p>
        {retry && (
          <Button
            size="small"
            variant="ghost"
            onClick={retry}
            className="shrink-0"
          >
            Retry
          </Button>
        )}
      </div>
    );
  }

  return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-6 space-y-3">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-6 h-6 text-red-600 shrink-0" />
        <div className="flex-1 space-y-2">
          <h3 className="text-size-2 font-semibold text-red-900">
            Something went wrong
          </h3>
          <p className="text-size-3 text-red-700">{errorMessage}</p>
        </div>
      </div>
      {retry && (
        <div className="flex justify-end">
          <Button
            variant="secondary"
            onClick={retry}
            size="small"
          >
            Try again
          </Button>
        </div>
      )}
    </div>
  );
}

interface EmptyStateProps {
  message?: string;
  icon?: React.ReactNode;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ 
  message = 'No data found',
  icon,
  action
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-12 space-y-4">
      {icon || <Inbox className="w-12 h-12 text-gray-400" />}
      <p className="text-size-3 text-gray-500 text-center">{message}</p>
      {action && (
        <Button
          variant="secondary"
          onClick={action.onClick}
          size="small"
        >
          {action.label}
        </Button>
      )}
    </div>
  );
}

/**
 * Inline loading indicator for buttons and small areas
 */
export function InlineLoader({ size = 16 }: { size?: number }) {
  return (
    <Loader2 
      className="animate-spin" 
      style={{ width: size, height: size }}
    />
  );
}

/**
 * Skeleton loader for content placeholders
 */
export function SkeletonLoader({ 
  lines = 3,
  className = ''
}: { 
  lines?: number;
  className?: string;
}) {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-4 bg-gray-200 rounded animate-pulse"
          style={{
            width: `${100 - (i * 10)}%`
          }}
        />
      ))}
    </div>
  );
}

/**
 * Progress bar for long-running operations
 */
export function ProgressBar({ 
  progress,
  label
}: { 
  progress: number;
  label?: string;
}) {
  const percentage = Math.min(100, Math.max(0, progress));

  return (
    <div className="space-y-2">
      {label && (
        <div className="flex justify-between items-center">
          <span className="text-size-4 text-gray-600">{label}</span>
          <span className="text-size-4 text-gray-600">{percentage}%</span>
        </div>
      )}
      <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className="h-full bg-blue-600 transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

/**
 * Retry message with countdown
 */
export function RetryMessage({ 
  onRetry,
  countdown = 5
}: { 
  onRetry: () => void;
  countdown?: number;
}) {
  const [seconds, setSeconds] = useState(countdown);

  useEffect(() => {
    if (seconds > 0) {
      const timer = setTimeout(() => setSeconds(seconds - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      onRetry();
    }
  }, [seconds, onRetry]);

  return (
    <div className="text-center space-y-2">
      <p className="text-size-3 text-gray-600">
        Retrying in {seconds} seconds...
      </p>
      <Button
        size="small"
        variant="ghost"
        onClick={() => {
          setSeconds(0);
          onRetry();
        }}
      >
        Retry now
      </Button>
    </div>
  );
}

import { useState, useEffect } from 'react';
