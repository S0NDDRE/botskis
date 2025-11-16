# 🏭 Botskis Factory Floor - Frontend

Visual control center for managing AI agents.

## Features

- 🎨 **2D Canvas View** - Drag & drop agents on factory floor
- 🎮 **Command Palette** - Quick commands (⌘K)
- 📊 **Real-time Metrics** - Live agent status
- 🔗 **Visual Connections** - See data flow between agents
- ⚡ **Marketplace** - 20+ agent templates
- 🎯 **One-click Deploy** - Drag from sidebar to deploy

## Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Usage

1. **Open**: http://localhost:3000
2. **Drag**: Agent from sidebar
3. **Drop**: Onto factory floor
4. **Command**: Press ⌘K for quick actions

## Tech Stack

- React 18 + TypeScript
- Vite
- Tailwind CSS
- Framer Motion (animations)
- React DnD (drag & drop)
- Zustand (state management)
- cmdk (command palette)

## Keyboard Shortcuts

- `⌘K` - Command palette
- `⌘R` - Refresh metrics
- `⌘1` - 2D view
- `⌘2` - 3D view (coming soon)

## Development

```bash
# Type checking
npm run build

# Lint
npm run lint
```
