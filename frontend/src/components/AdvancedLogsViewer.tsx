/**
 * Advanced Logs Viewer
 * Detailed logs viewer with filtering, search, and export
 */
import React, { useState, useEffect } from 'react';

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical';
  source: string;
  message: string;
  metadata?: Record<string, any>;
  stackTrace?: string;
}

interface LogsViewerProps {
  agentId?: string;
  source?: string;
}

export const AdvancedLogsViewer: React.FC<LogsViewerProps> = ({
  agentId,
  source
}) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([]);
  const [selectedLevel, setSelectedLevel] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [timeRange, setTimeRange] = useState('1h');

  // Mock data - would fetch from API in production
  useEffect(() => {
    const mockLogs: LogEntry[] = [
      {
        id: '1',
        timestamp: new Date().toISOString(),
        level: 'info',
        source: 'CustomerSupportAgent',
        message: 'Agent started successfully',
        metadata: { agentId: 'agent-123', version: '1.0.0' }
      },
      {
        id: '2',
        timestamp: new Date(Date.now() - 60000).toISOString(),
        level: 'debug',
        source: 'CustomerSupportAgent',
        message: 'Processing user query: "How do I reset my password?"',
        metadata: { userId: 'user-456', sessionId: 'sess-789' }
      },
      {
        id: '3',
        timestamp: new Date(Date.now() - 120000).toISOString(),
        level: 'warning',
        source: 'APIGateway',
        message: 'Rate limit approaching: 85% of quota used',
        metadata: { current: 8500, limit: 10000 }
      },
      {
        id: '4',
        timestamp: new Date(Date.now() - 180000).toISOString(),
        level: 'error',
        source: 'PaymentProcessor',
        message: 'Payment failed: Invalid card number',
        metadata: { orderId: 'ord-123', userId: 'user-456' },
        stackTrace: 'Error: Invalid card number\n  at validateCard (payment.ts:45)\n  at processPayment (payment.ts:120)'
      },
      {
        id: '5',
        timestamp: new Date(Date.now() - 240000).toISOString(),
        level: 'critical',
        source: 'Database',
        message: 'Connection pool exhausted',
        metadata: { poolSize: 100, activeConnections: 100 },
        stackTrace: 'Error: Connection pool exhausted\n  at getConnection (db.ts:34)\n  at query (db.ts:89)'
      }
    ];
    setLogs(mockLogs);
    setFilteredLogs(mockLogs);
  }, []);

  useEffect(() => {
    let filtered = logs;

    // Filter by level
    if (selectedLevel !== 'all') {
      filtered = filtered.filter(log => log.level === selectedLevel);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(log =>
        log.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
        log.source.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredLogs(filtered);
  }, [logs, selectedLevel, searchQuery]);

  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      // Fetch new logs (mock for now)
      console.log('Fetching new logs...');
    }, 5000);

    return () => clearInterval(interval);
  }, [autoRefresh]);

  const getLevelColor = (level: LogEntry['level']) => {
    switch (level) {
      case 'debug':
        return 'bg-gray-100 text-gray-800';
      case 'info':
        return 'bg-blue-100 text-blue-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      case 'critical':
        return 'bg-purple-100 text-purple-800';
    }
  };

  const getLevelIcon = (level: LogEntry['level']) => {
    switch (level) {
      case 'debug':
        return '🐛';
      case 'info':
        return 'ℹ️';
      case 'warning':
        return '⚠️';
      case 'error':
        return '❌';
      case 'critical':
        return '🔥';
    }
  };

  const exportLogs = (format: 'json' | 'csv') => {
    const logsToExport = filteredLogs;

    if (format === 'json') {
      const dataStr = JSON.stringify(logsToExport, null, 2);
      const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
      const exportFileDefaultName = `logs-${Date.now()}.json`;

      const linkElement = document.createElement('a');
      linkElement.setAttribute('href', dataUri);
      linkElement.setAttribute('download', exportFileDefaultName);
      linkElement.click();
    } else {
      // CSV format
      const headers = ['Timestamp', 'Level', 'Source', 'Message'];
      const csvContent = [
        headers.join(','),
        ...logsToExport.map(log =>
          [
            log.timestamp,
            log.level,
            log.source,
            `"${log.message.replace(/"/g, '""')}"`
          ].join(',')
        )
      ].join('\n');

      const dataUri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvContent);
      const exportFileDefaultName = `logs-${Date.now()}.csv`;

      const linkElement = document.createElement('a');
      linkElement.setAttribute('href', dataUri);
      linkElement.setAttribute('download', exportFileDefaultName);
      linkElement.click();
    }
  };

  const clearLogs = () => {
    if (confirm('Er du sikker på at du vil slette alle logs?')) {
      setLogs([]);
      setFilteredLogs([]);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg">
      {/* Header & Controls */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Logs</h2>
          <div className="flex items-center space-x-3">
            <label className="flex items-center space-x-2 text-sm">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                className="rounded"
              />
              <span>Auto-refresh (5s)</span>
            </label>
            <button
              onClick={() => exportLogs('json')}
              className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 text-sm"
            >
              Export JSON
            </button>
            <button
              onClick={() => exportLogs('csv')}
              className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 text-sm"
            >
              Export CSV
            </button>
            <button
              onClick={clearLogs}
              className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              Clear Logs
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-4">
          {/* Search */}
          <div className="flex-1">
            <input
              type="text"
              placeholder="Søk i logs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          {/* Level Filter */}
          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="all">Alle nivåer</option>
            <option value="debug">Debug</option>
            <option value="info">Info</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
            <option value="critical">Critical</option>
          </select>

          {/* Time Range */}
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="15m">Siste 15 min</option>
            <option value="1h">Siste time</option>
            <option value="24h">Siste 24 timer</option>
            <option value="7d">Siste 7 dager</option>
            <option value="30d">Siste 30 dager</option>
          </select>
        </div>
      </div>

      {/* Logs List */}
      <div className="h-96 overflow-y-auto">
        {filteredLogs.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <svg className="w-12 h-12 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p>Ingen logs funnet</p>
            </div>
          </div>
        ) : (
          filteredLogs.map((log) => (
            <div
              key={log.id}
              onClick={() => setSelectedLog(log)}
              className={`p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer ${
                selectedLog?.id === log.id ? 'bg-blue-50' : ''
              }`}
            >
              <div className="flex items-start space-x-3">
                <span className="text-2xl">{getLevelIcon(log.level)}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold ${getLevelColor(log.level)}`}>
                      {log.level.toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-500">{log.source}</span>
                    <span className="text-xs text-gray-400">
                      {new Date(log.timestamp).toLocaleString('no-NO')}
                    </span>
                  </div>
                  <p className="text-sm font-mono">{log.message}</p>
                  {log.metadata && (
                    <details className="mt-2">
                      <summary className="text-xs text-blue-600 cursor-pointer">Metadata</summary>
                      <pre className="text-xs bg-gray-100 p-2 rounded mt-1 overflow-x-auto">
                        {JSON.stringify(log.metadata, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Selected Log Details Modal */}
      {selectedLog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={() => setSelectedLog(null)}>
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[80vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <h3 className="text-xl font-bold">Log Details</h3>
              <button
                onClick={() => setSelectedLog(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="text-sm font-semibold text-gray-600">Level</label>
                <div className="mt-1">
                  <span className={`px-3 py-1 rounded text-sm font-semibold ${getLevelColor(selectedLog.level)}`}>
                    {selectedLog.level.toUpperCase()}
                  </span>
                </div>
              </div>
              <div>
                <label className="text-sm font-semibold text-gray-600">Timestamp</label>
                <p className="text-sm mt-1">{new Date(selectedLog.timestamp).toLocaleString('no-NO')}</p>
              </div>
              <div>
                <label className="text-sm font-semibold text-gray-600">Source</label>
                <p className="text-sm mt-1">{selectedLog.source}</p>
              </div>
              <div>
                <label className="text-sm font-semibold text-gray-600">Message</label>
                <p className="text-sm mt-1 font-mono bg-gray-100 p-3 rounded">{selectedLog.message}</p>
              </div>
              {selectedLog.metadata && (
                <div>
                  <label className="text-sm font-semibold text-gray-600">Metadata</label>
                  <pre className="text-sm mt-1 bg-gray-100 p-3 rounded overflow-x-auto">
                    {JSON.stringify(selectedLog.metadata, null, 2)}
                  </pre>
                </div>
              )}
              {selectedLog.stackTrace && (
                <div>
                  <label className="text-sm font-semibold text-gray-600">Stack Trace</label>
                  <pre className="text-sm mt-1 bg-red-50 p-3 rounded overflow-x-auto text-red-800 font-mono">
                    {selectedLog.stackTrace}
                  </pre>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Summary Footer */}
      <div className="p-4 border-t border-gray-200 bg-gray-50 text-sm text-gray-600">
        Viser {filteredLogs.length} av {logs.length} logs
      </div>
    </div>
  );
};

export default AdvancedLogsViewer;
