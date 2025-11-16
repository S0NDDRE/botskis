/**
 * Sidebar - Agent Marketplace & Templates
 */
import { useState, useEffect } from 'react'
import { useDrag } from 'react-dnd'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Star, TrendingUp, X, ChevronLeft, ChevronRight } from 'lucide-react'
import { useFactoryStore } from '@/store/factoryStore'
import type { AgentTemplate } from '@/types'

function TemplateCard({ template }: { template: AgentTemplate }) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'TEMPLATE',
    item: { id: template.id, type: 'TEMPLATE' },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }))

  return (
    <motion.div
      ref={drag}
      layout
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className={`
        relative bg-factory-machine hover:bg-factory-active rounded-lg p-3 cursor-grab
        border border-gray-700 hover:border-blue-500 transition-all
        ${isDragging ? 'opacity-50 scale-95' : 'opacity-100'}
      `}
    >
      {/* Template icon & info */}
      <div className="flex items-start gap-3">
        <div className="text-3xl">{template.icon}</div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="text-white font-semibold text-sm truncate">{template.name}</h4>
            {template.is_featured && (
              <Star className="w-3 h-3 text-yellow-400 fill-yellow-400 flex-shrink-0" />
            )}
          </div>
          <p className="text-gray-400 text-xs line-clamp-2 mb-2">{template.description}</p>

          {/* Stats */}
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <div className="flex items-center gap-1">
              <TrendingUp className="w-3 h-3" />
              <span>{template.deployment_count}</span>
            </div>
            <div className="flex items-center gap-1">
              <Star className="w-3 h-3" />
              <span>{template.rating}</span>
            </div>
          </div>

          {/* Category badge */}
          <div className="mt-2">
            <span className="inline-block px-2 py-0.5 bg-blue-500/20 text-blue-400 text-xs rounded">
              {template.category}
            </span>
          </div>
        </div>
      </div>

      {/* Drag hint */}
      {isDragging && (
        <div className="absolute inset-0 bg-blue-500/20 border-2 border-dashed border-blue-500 rounded-lg flex items-center justify-center">
          <div className="text-blue-400 text-xs font-semibold">Dragging...</div>
        </div>
      )}
    </motion.div>
  )
}

export function Sidebar() {
  const { templates, loadTemplates } = useFactoryStore()
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  useEffect(() => {
    loadTemplates()
  }, [])

  // Filter templates
  const filteredTemplates = templates.filter((t) => {
    const matchesSearch =
      searchQuery === '' ||
      t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.description.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesCategory = selectedCategory === 'all' || t.category === selectedCategory

    return matchesSearch && matchesCategory
  })

  // Get unique categories
  const categories = ['all', ...Array.from(new Set(templates.map((t) => t.category)))]

  // Featured templates
  const featuredTemplates = templates.filter((t) => t.is_featured)

  return (
    <>
      {/* Collapse toggle */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute left-0 top-1/2 -translate-y-1/2 z-30 bg-factory-machine hover:bg-factory-active p-2 rounded-r-lg transition-colors"
      >
        {isCollapsed ? (
          <ChevronRight className="w-4 h-4 text-white" />
        ) : (
          <ChevronLeft className="w-4 h-4 text-white" />
        )}
      </button>

      <motion.div
        animate={{ width: isCollapsed ? 0 : 320 }}
        className="relative h-full bg-factory-machine border-r border-gray-700 overflow-hidden"
      >
        <div className="w-80 h-full flex flex-col p-4">
          {/* Header */}
          <div className="mb-4">
            <h2 className="text-white text-xl font-bold mb-1">🏪 Agent Marketplace</h2>
            <p className="text-gray-400 text-sm">Drag & drop to deploy</p>
          </div>

          {/* Search */}
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search agents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-10 py-2 bg-factory-floor border border-gray-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2"
              >
                <X className="w-4 h-4 text-gray-400 hover:text-white" />
              </button>
            )}
          </div>

          {/* Categories */}
          <div className="flex flex-wrap gap-1 mb-4">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`
                  px-2 py-1 text-xs rounded transition-colors
                  ${
                    selectedCategory === cat
                      ? 'bg-blue-500 text-white'
                      : 'bg-factory-floor text-gray-400 hover:text-white'
                  }
                `}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Featured section */}
          {selectedCategory === 'all' && searchQuery === '' && featuredTemplates.length > 0 && (
            <div className="mb-4">
              <div className="flex items-center gap-2 mb-2">
                <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                <h3 className="text-white font-semibold text-sm">Featured</h3>
              </div>
              <div className="space-y-2">
                {featuredTemplates.slice(0, 3).map((template) => (
                  <TemplateCard key={template.id} template={template} />
                ))}
              </div>
              <div className="border-t border-gray-700 my-4"></div>
            </div>
          )}

          {/* Templates list */}
          <div className="flex-1 overflow-y-auto space-y-2">
            <AnimatePresence>
              {filteredTemplates.length > 0 ? (
                filteredTemplates.map((template) => (
                  <TemplateCard key={template.id} template={template} />
                ))
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center text-gray-500 py-8"
                >
                  <div className="text-4xl mb-2">🔍</div>
                  <p className="text-sm">No agents found</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Footer stats */}
          <div className="mt-4 pt-4 border-t border-gray-700">
            <div className="grid grid-cols-2 gap-2 text-center text-sm">
              <div>
                <div className="text-gray-400">Total</div>
                <div className="text-white font-semibold">{templates.length}</div>
              </div>
              <div>
                <div className="text-gray-400">Categories</div>
                <div className="text-white font-semibold">{categories.length - 1}</div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </>
  )
}
