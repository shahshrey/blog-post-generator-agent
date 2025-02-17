'use client'

import { Component, ErrorInfo, ReactNode } from 'react'
import { THEME } from '@/styles/theme'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div 
          className="flex flex-col items-center justify-center min-h-screen p-4"
          style={{ 
            backgroundColor: THEME.colors.background,
            color: THEME.colors.text 
          }}
        >
          <h2 className="text-2xl font-bold mb-4">Something went wrong</h2>
          <p className="text-sm text-gray-500 mb-4">
            {this.state.error?.message}
          </p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 rounded"
            style={{ backgroundColor: THEME.colors.primary, color: '#fff' }}
          >
            Try again
          </button>
        </div>
      )
    }

    return this.props.children
  }
} 