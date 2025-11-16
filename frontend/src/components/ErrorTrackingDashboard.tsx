/**
 * Error Tracking Dashboard
 * Self-hosted error monitoring (replaces Sentry)
 */
import React, { useState, useEffect } from 'react'
import { useTranslation } from '../i18n/translations'

// ============================================================================
// TYPES
// ============================================================================

type ErrorSeverity = 'debug' | 'info' | 'warning' | 'error' | 'critical'

interface ErrorEvent {
  error_id: string
  error_type: string
  error_message: string
  stack_trace: string
  fingerprint: string
  severity: ErrorSeverity
  resolved: boolean
  occurrences: number
  first_seen: string
  last_seen: string
  affected_users: number[]
  context: {
    user_id?: number
    request_id?: string
    url?: string
    method?: string
    ip_address?: string
    user_agent?: string
    environment: string
  }
}

interface ErrorStats {
  total_errors: number
  total_occurrences: number
  unresolved: number
  critical: number
  by_severity: Record<string, number>
  top_errors: Array<{
    error_id: string
    type: string
    message: string
    occurrences: number
    severity: ErrorSeverity
    affected_users: number
  }>
  affected_users_count: number
}

interface Trend {
  date: string
  total_errors: number
  total_occurrences: number
  critical: number
  errors: number
  warnings: number
}

// ============================================================================
// ERROR TRACKING DASHBOARD
// ============================================================================

export const ErrorTrackingDashboard: React.FC = () => {
  const { t } = useTranslation()

  // State
  const [stats, setStats] = useState<ErrorStats | null>(null)
  const [errors, setErrors] = useState<ErrorEvent[]>([])
  const [trends, setTrends] = useState<Trend[]>([])
  const [selectedError, setSelectedError] = useState<ErrorEvent | null>(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState({
    severity: '' as ErrorSeverity | '',
    resolved: '' as 'true' | 'false' | '',
    searchQuery: ''
  })

  // Fetch data
  useEffect(() => {
    fetchStats()
    fetchErrors()
    fetchTrends()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/errors/stats/overview')
      const data = await response.json()
      if (data.success) {
        setStats(data.stats)
      }
    } catch (error) {
      console.error('Failed to fetch error stats:', error)
    }
  }

  const fetchErrors = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (filter.severity) params.append('severity', filter.severity)
      if (filter.resolved) params.append('resolved', filter.resolved)

      const response = await fetch(`/api/errors/list?${params}`)
      const data = await response.json()
      if (data.success) {
        setErrors(data.errors)
      }
    } catch (error) {
      console.error('Failed to fetch errors:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTrends = async () => {
    try {
      const response = await fetch('/api/errors/stats/trends?days=7')
      const data = await response.json()
      if (data.success) {
        setTrends(data.trends)
      }
    } catch (error) {
      console.error('Failed to fetch trends:', error)
    }
  }

  const resolveError = async (fingerprint: string) => {
    try {
      const response = await fetch(`/api/errors/${fingerprint}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resolved_by: 1 }) // TODO: Get current user ID
      })
      const data = await response.json()
      if (data.success) {
        fetchErrors()
        fetchStats()
      }
    } catch (error) {
      console.error('Failed to resolve error:', error)
    }
  }

  const deleteError = async (fingerprint: string) => {
    if (!confirm('Are you sure? This cannot be undone.')) return

    try {
      const response = await fetch(`/api/errors/${fingerprint}`, {
        method: 'DELETE'
      })
      const data = await response.json()
      if (data.success) {
        fetchErrors()
        fetchStats()
        setSelectedError(null)
      }
    } catch (error) {
      console.error('Failed to delete error:', error)
    }
  }

  // Apply filters
  useEffect(() => {
    fetchErrors()
  }, [filter.severity, filter.resolved])

  // Filter errors by search query
  const filteredErrors = errors.filter(error => {
    if (!filter.searchQuery) return true
    const query = filter.searchQuery.toLowerCase()
    return (
      error.error_type.toLowerCase().includes(query) ||
      error.error_message.toLowerCase().includes(query)
    )
  })

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Error Tracking</h1>
          <p className="text-gray-600 mt-2">
            Self-hosted error monitoring and alerting
          </p>
        </div>

        {/* Statistics Overview */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Errors"
              value={stats.total_errors}
              change={0}
              icon="🐛"
            />
            <StatCard
              title="Total Occurrences"
              value={stats.total_occurrences}
              change={0}
              icon="🔢"
            />
            <StatCard
              title="Unresolved"
              value={stats.unresolved}
              change={0}
              icon="⚠️"
              highlight={stats.unresolved > 0}
            />
            <StatCard
              title="Critical"
              value={stats.critical}
              change={0}
              icon="🚨"
              highlight={stats.critical > 0}
              danger
            />
          </div>
        )}

        {/* Severity Breakdown */}
        {stats && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">By Severity</h2>
            <div className="grid grid-cols-5 gap-4">
              {Object.entries(stats.by_severity).map(([severity, count]) => (
                <div key={severity} className="text-center">
                  <div className={`text-3xl font-bold ${getSeverityColor(severity as ErrorSeverity)}`}>
                    {count}
                  </div>
                  <div className="text-sm text-gray-600 capitalize mt-1">
                    {severity}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Trends Chart */}
        {trends.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">7-Day Trend</h2>
            <div className="h-64 flex items-end space-x-2">
              {trends.map((trend, i) => {
                const maxOccurrences = Math.max(...trends.map(t => t.total_occurrences))
                const height = (trend.total_occurrences / maxOccurrences) * 100

                return (
                  <div key={i} className="flex-1 flex flex-col items-center">
                    <div className="w-full bg-gray-200 rounded-t relative" style={{ height: '200px' }}>
                      <div
                        className="w-full bg-red-500 rounded-t absolute bottom-0"
                        style={{ height: `${height}%` }}
                        title={`${trend.total_occurrences} occurrences`}
                      />
                    </div>
                    <div className="text-xs text-gray-600 mt-2">
                      {new Date(trend.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </div>
                    <div className="text-xs font-semibold text-gray-900">
                      {trend.total_occurrences}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Top Errors */}
        {stats && stats.top_errors.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">Top Errors (Most Frequent)</h2>
            <div className="space-y-3">
              {stats.top_errors.map((error, i) => (
                <div key={error.error_id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-4 flex-1">
                    <div className="text-2xl font-bold text-gray-400">#{i + 1}</div>
                    <div className="flex-1">
                      <div className="font-semibold text-gray-900">{error.type}</div>
                      <div className="text-sm text-gray-600 truncate">{error.message}</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">{error.occurrences}</div>
                      <div className="text-xs text-gray-600">occurrences</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">{error.affected_users}</div>
                      <div className="text-xs text-gray-600">users</div>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-xs font-semibold ${getSeverityBadge(error.severity)}`}>
                      {error.severity.toUpperCase()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <input
                type="text"
                value={filter.searchQuery}
                onChange={(e) => setFilter({ ...filter, searchQuery: e.target.value })}
                placeholder="Search error type or message..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Severity
              </label>
              <select
                value={filter.severity}
                onChange={(e) => setFilter({ ...filter, severity: e.target.value as ErrorSeverity | '' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Severities</option>
                <option value="critical">Critical</option>
                <option value="error">Error</option>
                <option value="warning">Warning</option>
                <option value="info">Info</option>
                <option value="debug">Debug</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={filter.resolved}
                onChange={(e) => setFilter({ ...filter, resolved: e.target.value as 'true' | 'false' | '' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Errors</option>
                <option value="false">Unresolved Only</option>
                <option value="true">Resolved Only</option>
              </select>
            </div>
          </div>
        </div>

        {/* Error List */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold">Error Events</h2>
          </div>

          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
              <p className="text-gray-600 mt-4">Loading errors...</p>
            </div>
          ) : filteredErrors.length === 0 ? (
            <div className="p-12 text-center">
              <div className="text-6xl mb-4">✅</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No errors found</h3>
              <p className="text-gray-600">Your application is running smoothly!</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredErrors.map((error) => (
                <ErrorRow
                  key={error.fingerprint}
                  error={error}
                  onSelect={() => setSelectedError(error)}
                  onResolve={() => resolveError(error.fingerprint)}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Error Detail Modal */}
      {selectedError && (
        <ErrorDetailModal
          error={selectedError}
          onClose={() => setSelectedError(null)}
          onResolve={() => {
            resolveError(selectedError.fingerprint)
            setSelectedError(null)
          }}
          onDelete={() => deleteError(selectedError.fingerprint)}
        />
      )}
    </div>
  )
}

// ============================================================================
// STAT CARD COMPONENT
// ============================================================================

interface StatCardProps {
  title: string
  value: number
  change: number
  icon: string
  highlight?: boolean
  danger?: boolean
}

const StatCard: React.FC<StatCardProps> = ({ title, value, change, icon, highlight, danger }) => {
  return (
    <div className={`bg-white rounded-lg shadow-sm p-6 ${highlight ? (danger ? 'ring-2 ring-red-500' : 'ring-2 ring-yellow-500') : ''}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-600 text-sm font-medium">{title}</span>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className="text-3xl font-bold text-gray-900">{value.toLocaleString()}</div>
    </div>
  )
}

// ============================================================================
// ERROR ROW COMPONENT
// ============================================================================

interface ErrorRowProps {
  error: ErrorEvent
  onSelect: () => void
  onResolve: () => void
}

const ErrorRow: React.FC<ErrorRowProps> = ({ error, onSelect, onResolve }) => {
  const timeSince = getTimeSince(error.last_seen)

  return (
    <div className="p-6 hover:bg-gray-50 cursor-pointer" onClick={onSelect}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <span className={`px-2 py-1 rounded text-xs font-semibold ${getSeverityBadge(error.severity)}`}>
              {error.severity.toUpperCase()}
            </span>
            {error.resolved && (
              <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-semibold">
                RESOLVED
              </span>
            )}
            <span className="text-sm text-gray-600">
              ID: {error.error_id}
            </span>
          </div>

          <h3 className="font-semibold text-gray-900 mb-1">{error.error_type}</h3>
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">{error.error_message}</p>

          <div className="flex items-center space-x-6 text-sm text-gray-600">
            <div>
              <span className="font-semibold">{error.occurrences}</span> occurrences
            </div>
            <div>
              <span className="font-semibold">{error.affected_users.length}</span> users affected
            </div>
            <div>Last seen {timeSince}</div>
            <div className="text-xs bg-gray-100 px-2 py-1 rounded">
              {error.context.environment}
            </div>
          </div>
        </div>

        {!error.resolved && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              onResolve()
            }}
            className="ml-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Resolve
          </button>
        )}
      </div>
    </div>
  )
}

// ============================================================================
// ERROR DETAIL MODAL
// ============================================================================

interface ErrorDetailModalProps {
  error: ErrorEvent
  onClose: () => void
  onResolve: () => void
  onDelete: () => void
}

const ErrorDetailModal: React.FC<ErrorDetailModalProps> = ({ error, onClose, onResolve, onDelete }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{error.error_type}</h2>
            <p className="text-sm text-gray-600 mt-1">Error ID: {error.error_id}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Badges */}
          <div className="flex items-center space-x-3">
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSeverityBadge(error.severity)}`}>
              {error.severity.toUpperCase()}
            </span>
            {error.resolved && (
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                RESOLVED
              </span>
            )}
          </div>

          {/* Message */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Error Message</h3>
            <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">{error.error_message}</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Occurrences</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">{error.occurrences}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Affected Users</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">{error.affected_users.length}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Environment</div>
              <div className="text-lg font-bold text-gray-900 mt-1">{error.context.environment}</div>
            </div>
          </div>

          {/* Timeline */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">First Seen</h3>
              <p className="text-gray-700">{new Date(error.first_seen).toLocaleString()}</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Last Seen</h3>
              <p className="text-gray-700">{new Date(error.last_seen).toLocaleString()}</p>
            </div>
          </div>

          {/* Context */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Context</h3>
            <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm">
              {error.context.url && <div><span className="font-semibold">URL:</span> {error.context.url}</div>}
              {error.context.method && <div><span className="font-semibold">Method:</span> {error.context.method}</div>}
              {error.context.user_id && <div><span className="font-semibold">User ID:</span> {error.context.user_id}</div>}
              {error.context.request_id && <div><span className="font-semibold">Request ID:</span> {error.context.request_id}</div>}
            </div>
          </div>

          {/* Stack Trace */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Stack Trace</h3>
            <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-xs">
              {error.stack_trace}
            </pre>
          </div>
        </div>

        {/* Actions */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex items-center justify-between">
          <button
            onClick={onDelete}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Delete Permanently
          </button>
          <div className="space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Close
            </button>
            {!error.resolved && (
              <button
                onClick={onResolve}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Mark as Resolved
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function getSeverityColor(severity: ErrorSeverity): string {
  const colors = {
    debug: 'text-gray-600',
    info: 'text-blue-600',
    warning: 'text-yellow-600',
    error: 'text-orange-600',
    critical: 'text-red-600'
  }
  return colors[severity] || 'text-gray-600'
}

function getSeverityBadge(severity: ErrorSeverity): string {
  const badges = {
    debug: 'bg-gray-100 text-gray-800',
    info: 'bg-blue-100 text-blue-800',
    warning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800'
  }
  return badges[severity] || 'bg-gray-100 text-gray-800'
}

function getTimeSince(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (seconds < 60) return 'just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`
  if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`
  return date.toLocaleDateString()
}

// ============================================================================
// EXPORT
// ============================================================================

export default ErrorTrackingDashboard
