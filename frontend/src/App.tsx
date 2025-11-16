/**
 * Main App - Factory Floor Control Center
 */
import { useEffect } from 'react'
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
import { FactoryFloor } from './components/FactoryFloor'
import { Sidebar } from './components/Sidebar'
import { CommandPalette } from './components/CommandPalette'
import { useFactoryStore } from './store/factoryStore'
import { Terminal, Zap, Eye } from 'lucide-react'

function App() {
  const { loadAgents, loadTemplates, toggleCommandPalette, refreshMetrics, viewMode, setViewMode } =
    useFactoryStore()

  // Load data on mount
  useEffect(() => {
    const userId = 1 // TODO: Get from auth
    loadAgents(userId)
    loadTemplates()
    refreshMetrics()

    // Refresh metrics every 10 seconds
    const interval = setInterval(() => {
      refreshMetrics()
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="w-screen h-screen bg-factory-floor flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-factory-machine border-b border-gray-700 px-6 py-3 flex items-center justify-between z-20">
          <div className="flex items-center gap-3">
            <div className="text-3xl">🏭</div>
            <div>
              <h1 className="text-white text-xl font-bold">Botskis Factory Floor</h1>
              <p className="text-gray-400 text-sm">Your AI Agent Control Center</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* View mode toggle */}
            <div className="flex bg-factory-floor rounded-lg p-1">
              <button
                onClick={() => setViewMode('2d')}
                className={`px-3 py-1.5 rounded text-sm transition-colors ${
                  viewMode === '2d'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                2D View
              </button>
              <button
                onClick={() => setViewMode('3d')}
                className={`px-3 py-1.5 rounded text-sm transition-colors ${
                  viewMode === '3d'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
                title="3D View (Coming Soon)"
              >
                3D View
              </button>
            </div>

            {/* Command palette button */}
            <button
              onClick={toggleCommandPalette}
              className="flex items-center gap-2 px-4 py-2 bg-factory-floor hover:bg-factory-active rounded-lg transition-colors"
            >
              <Terminal className="w-4 h-4 text-white" />
              <span className="text-white text-sm">Command</span>
              <kbd className="px-2 py-0.5 text-xs text-gray-400 bg-gray-800 rounded">⌘K</kbd>
            </button>

            {/* Quick actions */}
            <div className="flex gap-1">
              <button
                onClick={() => refreshMetrics()}
                className="p-2 bg-factory-floor hover:bg-factory-active rounded-lg transition-colors"
                title="Refresh Metrics"
              >
                <Zap className="w-4 h-4 text-yellow-400" />
              </button>
            </div>
          </div>
        </header>

        {/* Main content */}
        <div className="flex-1 flex overflow-hidden relative">
          {/* Sidebar */}
          <Sidebar />

          {/* Factory Floor */}
          <div className="flex-1 relative">
            {viewMode === '2d' ? (
              <FactoryFloor />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-factory-floor">
                <div className="text-center text-gray-500">
                  <Eye className="w-16 h-16 mx-auto mb-4 text-gray-600" />
                  <h3 className="text-xl font-semibold mb-2">3D View Coming Soon</h3>
                  <p className="text-sm">Experience your factory floor in stunning 3D</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Command Palette */}
        <CommandPalette />

        {/* Status bar */}
        <footer className="bg-factory-machine border-t border-gray-700 px-6 py-2 flex items-center justify-between text-xs text-gray-400 z-20">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span>System Online</span>
            </div>
            <div>API: http://localhost:8000</div>
          </div>
          <div className="flex items-center gap-4">
            <span>Press ⌘K for commands</span>
            <span>Drag agents from sidebar</span>
            <span>v1.0.0</span>
          </div>
        </footer>
      </div>
    </DndProvider>
  )
}

export default App
