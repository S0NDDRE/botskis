/**
 * CommandPalette - Quick command interface for Factory Chief
 */
import { useEffect, useState, useMemo } from 'react'
import { Command } from 'cmdk'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Search,
  Play,
  Pause,
  Trash2,
  Plus,
  Settings,
  Activity,
  BarChart3,
  Zap,
  Eye,
  EyeOff,
} from 'lucide-react'
import { useFactoryStore } from '@/store/factoryStore'
import type { CommandAction } from '@/types'

export function CommandPalette() {
  const {
    isCommandPaletteOpen,
    toggleCommandPalette,
    agents,
    templates,
    pauseAgent,
    resumeAgent,
    deleteAgent,
    deployAgent,
    setViewMode,
    refreshMetrics,
  } = useFactoryStore()

  const [search, setSearch] = useState('')

  // Build command actions
  const commands = useMemo<CommandAction[]>(() => {
    const actions: CommandAction[] = []

    // Agent control commands
    agents.forEach((agent) => {
      // Pause/Resume
      if (agent.status === 'active') {
        actions.push({
          id: `pause-${agent.id}`,
          label: `Pause ${agent.name}`,
          icon: 'pause',
          command: `/pause ${agent.name}`,
          action: () => pauseAgent(agent.id),
          shortcut: undefined,
        })
      } else if (agent.status === 'paused') {
        actions.push({
          id: `resume-${agent.id}`,
          label: `Resume ${agent.name}`,
          icon: 'play',
          command: `/resume ${agent.name}`,
          action: () => resumeAgent(agent.id),
          shortcut: undefined,
        })
      }

      // Delete
      actions.push({
        id: `delete-${agent.id}`,
        label: `Delete ${agent.name}`,
        icon: 'trash',
        command: `/delete ${agent.name}`,
        action: () => {
          if (confirm(`Delete ${agent.name}?`)) {
            deleteAgent(agent.id)
          }
        },
        shortcut: undefined,
      })
    })

    // Deploy commands
    templates.slice(0, 10).forEach((template) => {
      actions.push({
        id: `deploy-${template.id}`,
        label: `Deploy ${template.name}`,
        icon: 'plus',
        command: `/deploy ${template.name}`,
        action: () => {
          deployAgent(template.id, { x: 100 + Math.random() * 400, y: 100 + Math.random() * 400 })
        },
        shortcut: undefined,
      })
    })

    // System commands
    actions.push(
      {
        id: 'pause-all',
        label: 'Pause All Agents',
        icon: 'pause',
        command: '/pause-all',
        action: () => {
          agents.forEach((a) => {
            if (a.status === 'active') pauseAgent(a.id)
          })
        },
        shortcut: '⌘⇧P',
      },
      {
        id: 'resume-all',
        label: 'Resume All Agents',
        icon: 'play',
        command: '/resume-all',
        action: () => {
          agents.forEach((a) => {
            if (a.status === 'paused') resumeAgent(a.id)
          })
        },
        shortcut: '⌘⇧R',
      },
      {
        id: 'refresh-metrics',
        label: 'Refresh Metrics',
        icon: 'activity',
        command: '/refresh',
        action: () => refreshMetrics(),
        shortcut: '⌘R',
      },
      {
        id: 'view-2d',
        label: 'Switch to 2D View',
        icon: 'eye',
        command: '/view 2d',
        action: () => setViewMode('2d'),
        shortcut: '⌘1',
      },
      {
        id: 'view-3d',
        label: 'Switch to 3D View',
        icon: 'eye-off',
        command: '/view 3d',
        action: () => setViewMode('3d'),
        shortcut: '⌘2',
      }
    )

    return actions
  }, [agents, templates])

  // Keyboard shortcut to open/close
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        toggleCommandPalette()
      }
    }

    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  const icons: Record<string, any> = {
    pause: Pause,
    play: Play,
    trash: Trash2,
    plus: Plus,
    settings: Settings,
    activity: Activity,
    chart: BarChart3,
    zap: Zap,
    eye: Eye,
    'eye-off': EyeOff,
  }

  return (
    <AnimatePresence>
      {isCommandPaletteOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleCommandPalette}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          />

          {/* Command Palette */}
          <motion.div
            initial={{ opacity: 0, y: -20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            className="fixed top-[20%] left-1/2 -translate-x-1/2 w-full max-w-2xl z-50"
          >
            <Command
              className="bg-factory-machine border border-gray-700 rounded-lg shadow-2xl overflow-hidden"
              label="Command Menu"
            >
              {/* Search input */}
              <div className="flex items-center border-b border-gray-700 px-4">
                <Search className="w-5 h-5 text-gray-400 mr-3" />
                <Command.Input
                  value={search}
                  onValueChange={setSearch}
                  placeholder="Type a command or search..."
                  className="w-full py-4 bg-transparent text-white placeholder-gray-500 outline-none"
                />
                <kbd className="px-2 py-1 text-xs text-gray-400 bg-gray-800 rounded">ESC</kbd>
              </div>

              {/* Command list */}
              <Command.List className="max-h-96 overflow-y-auto p-2">
                {/* No results */}
                <Command.Empty className="py-6 text-center text-gray-500">
                  No results found.
                </Command.Empty>

                {/* Agent Controls */}
                {agents.length > 0 && (
                  <Command.Group
                    heading="Agent Controls"
                    className="mb-2 px-2 py-1.5 text-xs font-semibold text-gray-400"
                  >
                    {commands
                      .filter((c) => c.id.startsWith('pause-') || c.id.startsWith('resume-') || c.id.startsWith('delete-'))
                      .map((cmd) => {
                        const Icon = icons[cmd.icon]
                        return (
                          <Command.Item
                            key={cmd.id}
                            onSelect={() => {
                              cmd.action()
                              toggleCommandPalette()
                            }}
                            className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-factory-active transition-colors data-[selected]:bg-factory-active"
                          >
                            <Icon className="w-4 h-4 text-gray-400" />
                            <div className="flex-1">
                              <div className="text-white text-sm">{cmd.label}</div>
                              <div className="text-gray-500 text-xs">{cmd.command}</div>
                            </div>
                            {cmd.shortcut && (
                              <kbd className="px-2 py-1 text-xs text-gray-400 bg-gray-800 rounded">
                                {cmd.shortcut}
                              </kbd>
                            )}
                          </Command.Item>
                        )
                      })}
                  </Command.Group>
                )}

                {/* Deploy Agents */}
                <Command.Group
                  heading="Deploy Agents"
                  className="mb-2 px-2 py-1.5 text-xs font-semibold text-gray-400"
                >
                  {commands
                    .filter((c) => c.id.startsWith('deploy-'))
                    .map((cmd) => {
                      const Icon = icons[cmd.icon]
                      return (
                        <Command.Item
                          key={cmd.id}
                          onSelect={() => {
                            cmd.action()
                            toggleCommandPalette()
                          }}
                          className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-factory-active transition-colors data-[selected]:bg-factory-active"
                        >
                          <Icon className="w-4 h-4 text-gray-400" />
                          <div className="flex-1">
                            <div className="text-white text-sm">{cmd.label}</div>
                            <div className="text-gray-500 text-xs">{cmd.command}</div>
                          </div>
                        </Command.Item>
                      )
                    })}
                </Command.Group>

                {/* System Commands */}
                <Command.Group
                  heading="System"
                  className="mb-2 px-2 py-1.5 text-xs font-semibold text-gray-400"
                >
                  {commands
                    .filter((c) => !c.id.includes('-'))
                    .map((cmd) => {
                      const Icon = icons[cmd.icon]
                      return (
                        <Command.Item
                          key={cmd.id}
                          onSelect={() => {
                            cmd.action()
                            toggleCommandPalette()
                          }}
                          className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-factory-active transition-colors data-[selected]:bg-factory-active"
                        >
                          <Icon className="w-4 h-4 text-gray-400" />
                          <div className="flex-1">
                            <div className="text-white text-sm">{cmd.label}</div>
                            <div className="text-gray-500 text-xs">{cmd.command}</div>
                          </div>
                          {cmd.shortcut && (
                            <kbd className="px-2 py-1 text-xs text-gray-400 bg-gray-800 rounded">
                              {cmd.shortcut}
                            </kbd>
                          )}
                        </Command.Item>
                      )
                    })}
                </Command.Group>
              </Command.List>

              {/* Footer */}
              <div className="border-t border-gray-700 px-4 py-2 text-xs text-gray-500 flex items-center justify-between">
                <div>
                  <kbd className="px-1.5 py-0.5 bg-gray-800 rounded mr-1">↑↓</kbd> Navigate
                  <kbd className="px-1.5 py-0.5 bg-gray-800 rounded ml-2 mr-1">↵</kbd> Select
                </div>
                <div>
                  <kbd className="px-1.5 py-0.5 bg-gray-800 rounded">⌘K</kbd> Toggle
                </div>
              </div>
            </Command>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
