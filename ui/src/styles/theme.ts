export const THEME = {
  colors: {
    // Base colors
    primary: 'var(--color-primary)',
    secondary: 'var(--color-secondary)',
    background: 'var(--color-background)',
    text: 'var(--color-text)',
    border: 'var(--color-border)',
    error: 'var(--color-error)',
    success: 'var(--color-success)',
    
    // Semantic mappings for Tailwind/shadcn
    input: 'var(--color-border)',
    ring: 'var(--color-primary)',
    foreground: 'var(--color-text)',
    'muted-foreground': 'var(--color-text-muted)',
    'primary-foreground': 'var(--color-text-on-primary)',
    'secondary-foreground': 'var(--color-text-on-secondary)',
    accent: 'var(--color-accent)',
    'accent-foreground': 'var(--color-text-on-accent)',
    destructive: 'var(--color-error)',
    'destructive-foreground': 'var(--color-text-on-error)',
  },
  spacing: {
    xs: 'var(--spacing-xs)',
    sm: 'var(--spacing-sm)', 
    md: 'var(--spacing-md)',
    lg: 'var(--spacing-lg)',
    xl: 'var(--spacing-xl)',
  },
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
  },
} as const;

export type Theme = typeof THEME; 