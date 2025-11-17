/**
 * React Error Boundary
 * Automatically captures and reports frontend errors
 */
import React, { Component, ErrorInfo, ReactNode } from 'react'

// ============================================================================
// TYPES
// ============================================================================

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

// ============================================================================
// ERROR BOUNDARY COMPONENT
// ============================================================================

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Update state so the next render will show the fallback UI
    return {
      hasError: true,
      error
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to our error tracking system
    this.setState({ errorInfo })

    // Capture error
    this.captureError(error, errorInfo)

    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }
  }

  async captureError(error: Error, errorInfo: ErrorInfo) {
    try {
      // Get user info (if available)
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null

      // Capture exception to backend
      await fetch('/api/errors/capture/exception', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          error_type: error.name,
          error_message: error.message,
          stack_trace: error.stack || errorInfo.componentStack,
          severity: 'error',
          context: {
            user_id: user?.id,
            url: window.location.href,
            user_agent: navigator.userAgent,
            environment: process.env.NODE_ENV || 'production',
            additional_data: {
              component_stack: errorInfo.componentStack,
              browser: navigator.userAgent,
              viewport: `${window.innerWidth}x${window.innerHeight}`,
              timestamp: new Date().toISOString()
            }
          }
        })
      })
    } catch (e) {
      // Fallback: log to console if error tracking fails
      console.error('Failed to report error to error tracking:', e)
      console.error('Original error:', error)
    }
  }

  resetError = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    })
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Default fallback UI
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">⚠️</div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Oops! Something went wrong
              </h1>
              <p className="text-gray-600">
                We're sorry for the inconvenience. The error has been automatically reported to our team.
              </p>
            </div>

            {/* Error details (only in development) */}
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <div className="mb-6">
                <details className="bg-gray-50 p-4 rounded-lg">
                  <summary className="cursor-pointer font-semibold text-gray-900 mb-2">
                    Error Details (Development Only)
                  </summary>
                  <div className="mt-4 space-y-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">Error:</h3>
                      <p className="text-red-600 font-mono text-sm">
                        {this.state.error.toString()}
                      </p>
                    </div>
                    {this.state.error.stack && (
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-1">Stack Trace:</h3>
                        <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-xs">
                          {this.state.error.stack}
                        </pre>
                      </div>
                    )}
                    {this.state.errorInfo && (
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-1">Component Stack:</h3>
                        <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-xs">
                          {this.state.errorInfo.componentStack}
                        </pre>
                      </div>
                    )}
                  </div>
                </details>
              </div>
            )}

            {/* Actions */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={this.resetError}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                Try Again
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-semibold"
              >
                Go to Home
              </button>
            </div>

            {/* Contact support */}
            <div className="mt-8 text-center text-sm text-gray-600">
              <p>
                If the problem persists, please{' '}
                <a href="/support" className="text-blue-600 hover:underline">
                  contact support
                </a>
              </p>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// ============================================================================
// GLOBAL ERROR HANDLER (for uncaught errors)
// ============================================================================

export const setupGlobalErrorHandlers = () => {
  // Capture unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)

    // Send to error tracking
    fetch('/api/errors/capture/exception', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        error_type: 'UnhandledPromiseRejection',
        error_message: event.reason?.message || String(event.reason),
        stack_trace: event.reason?.stack || 'No stack trace available',
        severity: 'error',
        context: {
          url: window.location.href,
          user_agent: navigator.userAgent,
          environment: process.env.NODE_ENV || 'production'
        }
      })
    }).catch(err => console.error('Failed to report unhandled rejection:', err))
  })

  // Capture global errors
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error)

    // Send to error tracking
    fetch('/api/errors/capture/exception', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        error_type: event.error?.name || 'Error',
        error_message: event.error?.message || event.message,
        stack_trace: event.error?.stack || `at ${event.filename}:${event.lineno}:${event.colno}`,
        severity: 'error',
        context: {
          url: window.location.href,
          user_agent: navigator.userAgent,
          environment: process.env.NODE_ENV || 'production',
          additional_data: {
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno
          }
        }
      })
    }).catch(err => console.error('Failed to report global error:', err))
  })

  console.log('✅ Global error handlers initialized')
}

// ============================================================================
// EXPORT
// ============================================================================

export default ErrorBoundary
