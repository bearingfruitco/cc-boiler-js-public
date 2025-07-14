import { cn } from '@/lib/utils';

interface PageLayoutProps {
  children: React.ReactNode;
  className?: string;
  background?: 'white' | 'gray' | 'gradient';
}

export function PageLayout({ 
  children, 
  className,
  background = 'gray'
}: PageLayoutProps) {
  const backgrounds = {
    white: 'bg-white',
    gray: 'bg-gray-50',
    gradient: 'bg-gradient-to-b from-gray-50 to-white'
  };
  
  return (
    <div className={cn(
      'min-h-screen',
      backgrounds[background],
      className
    )}>
      {children}
    </div>
  );
}
