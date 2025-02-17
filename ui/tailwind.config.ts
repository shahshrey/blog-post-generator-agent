import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";
import animate from "tailwindcss-animate";

export default {
    darkMode: ["class"],
    content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
  	extend: {
  		colors: {
  			// Base colors
  			primary: {
  				DEFAULT: 'var(--color-primary)',
  				foreground: 'var(--color-text-on-primary)'
  			},
  			secondary: {
  				DEFAULT: 'var(--color-secondary)',
  				foreground: 'var(--color-text-on-secondary)'
  			},
  			background: 'var(--color-background)',
  			foreground: 'var(--color-text)',
  			border: 'var(--color-border)',
  			
  			// Semantic colors
  			muted: {
  				DEFAULT: 'var(--color-text-muted)',
  				foreground: 'var(--color-text-muted)'
  			},
  			accent: {
  				DEFAULT: 'var(--color-accent)',
  				foreground: 'var(--color-text-on-accent)'
  			},
  			destructive: {
  				DEFAULT: 'var(--color-error)',
  				foreground: 'var(--color-text-on-error)'
  			},
  			success: 'var(--color-success)',
  			input: 'var(--color-border)',
  			ring: 'var(--color-primary)',
  			
  			// Chart colors (preserved from original config)
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			}
  		},
  		typography: {
  			DEFAULT: {
  				css: {
  					maxWidth: 'none',
  					color: 'inherit',
  					a: {
  						color: 'inherit',
  						textDecoration: 'none',
  						fontWeight: '500'
  					},
  					strong: {
  						color: 'inherit'
  					},
  					h1: {
  						color: 'inherit'
  					},
  					h2: {
  						color: 'inherit'
  					},
  					h3: {
  						color: 'inherit'
  					},
  					h4: {
  						color: 'inherit'
  					},
  					code: {
  						color: 'inherit'
  					}
  				}
  			}
  		},
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		}
  	}
  },
  plugins: [
    typography,
    animate
  ],
} satisfies Config;
