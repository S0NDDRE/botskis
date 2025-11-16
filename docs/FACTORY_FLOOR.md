# 🏭 Factory Floor - Visual Control Center

## Oversikt

**Factory Floor** er ditt visuelle styringssystem for AI-agenter. Som "Fabrikksjef" kan du:

- 👁️ **Se alt** - Visuell oversikt over alle agenter
- 🎯 **Dra og slipp** - Deploy agenter med drag & drop
- ⌨️ **Gi kommandoer** - Direkte kontroll via Command Palette
- 📊 **Monitor** - Real-time metrics og status
- 🔗 **Visualiser** - Se data-flow mellom agenter

## Funksjoner

### 1. 2D Canvas View

```
┌────────────────────────────────────────────┐
│  🏭 Factory Floor                          │
│                                            │
│   [📧 Email Bot]──────►[📋 Trello]        │
│         │                                  │
│         ▼                                  │
│   [Filter]                                 │
│                                            │
│   [💼 Sales Bot]──────►[📅 Calendar]      │
│                                            │
└────────────────────────────────────────────┘
```

**Features:**
- Grid-based layout
- Zoom & pan controls
- Connection visualization
- Animated data flow
- Status indicators

### 2. Agent Cards

Hver agent vises som et kort med:
- **Status** - Active 🟢, Paused 🟡, Error 🔴, Healing 🔵
- **Metrics** - Runs, Success rate, Errors
- **Controls** - Pause/Resume, Settings, Delete
- **Connection points** - For visual linking

### 3. Command Palette (⌘K)

Quick commands for power users:

```
/pause email-bot        → Pause specific agent
/resume all             → Resume all agents
/deploy sales-bot       → Deploy new agent
/refresh                → Refresh metrics
/view 3d                → Switch to 3D view
```

**Shortcuts:**
- `⌘K` - Open command palette
- `⌘R` - Refresh metrics
- `⌘⇧P` - Pause all
- `⌘⇧R` - Resume all
- `⌘1` - 2D view
- `⌘2` - 3D view

### 4. Marketplace Sidebar

- **Search** - Find agents quickly
- **Categories** - Filter by type
- **Featured** - Highlighted templates
- **Drag & Drop** - Deploy instantly

### 5. Real-time Updates

- Live agent status
- Metrics refresh every 10s
- Connection status
- Error notifications

## Arkitektur

```
frontend/
├── src/
│   ├── components/
│   │   ├── FactoryFloor.tsx    # Main canvas
│   │   ├── AgentCard.tsx       # Agent visualization
│   │   ├── Sidebar.tsx         # Marketplace
│   │   └── CommandPalette.tsx  # Command interface
│   ├── store/
│   │   └── factoryStore.ts     # State management
│   ├── api/
│   │   └── client.ts           # Backend API
│   ├── types/
│   │   └── index.ts            # TypeScript types
│   ├── App.tsx                 # Main app
│   └── main.tsx                # Entry point
├── package.json
└── vite.config.ts
```

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React DnD** - Drag & drop
- **Zustand** - State management
- **cmdk** - Command palette
- **Axios** - HTTP client

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
# Open http://localhost:3000
```

### Production

```bash
npm run build
npm run preview
```

## Usage Guide

### Deploy an Agent

**Method 1: Drag & Drop**
1. Find agent in sidebar
2. Drag to factory floor
3. Drop where you want it
4. Agent deploys instantly

**Method 2: Command Palette**
1. Press `⌘K`
2. Type "deploy"
3. Select agent template
4. Agent deploys at random position

### Control Agents

**Pause/Resume:**
- Click pause button on agent card
- Or use command: `/pause agent-name`

**Delete:**
- Click delete button
- Confirm deletion
- Or command: `/delete agent-name`

**Configure:**
- Click settings button
- Opens detail panel
- Adjust configuration

### Monitor Performance

**Agent Metrics:**
- Runs today
- Success rate
- Error count
- Last run time

**System Metrics:**
- Total agents
- Active agents
- Errors today
- Avg response time

### Visual Connections

**Create Connection:**
1. Click connection point on agent
2. Drag to target agent
3. Release to create link
4. See animated data flow

**Remove Connection:**
- Click connection line
- Press Delete or Backspace

## UI/UX Features

### Animations

- **Agent deploy** - Scale & rotate entrance
- **Hover** - Scale up on hover
- **Drag** - Opacity change
- **Connections** - Animated flow
- **Status** - Pulsing indicators

### Colors

```css
Active:   Green  (#22c55e)
Paused:   Yellow (#f59e0b)
Error:    Red    (#ef4444)
Healing:  Blue   (#3b82f6)
```

### Responsive

- Sidebar collapsible
- Adaptive grid
- Touch support (basic)

## API Integration

Factory Floor connects to backend:

```typescript
// Get agents
GET /api/v1/agents?user_id=1

// Deploy agent
POST /api/v1/agents/deploy

// Pause agent
POST /api/v1/agents/{id}/pause

// Get metrics
GET /metrics
```

## Future Features

### 3D View (Planned)

- Three.js integration
- Isometric factory floor
- Agent "machines"
- 3D connections
- Camera controls

### Advanced Features

- [ ] Agent grouping
- [ ] Template customization
- [ ] Workflow builder
- [ ] A/B testing
- [ ] Team collaboration
- [ ] Custom dashboards

## Performance

- **Initial load**: <2s
- **Agent deploy**: <500ms
- **Drag response**: 60fps
- **Metrics update**: 10s interval

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Accessibility

- Keyboard navigation
- Screen reader support
- High contrast mode
- Focus indicators

## Troubleshooting

### Agent not deploying

Check:
1. Backend is running
2. Network connection
3. Browser console for errors

### Drag & drop not working

Check:
1. Browser compatibility
2. JavaScript enabled
3. Try refresh page

### Metrics not updating

Check:
1. API endpoint accessible
2. Network tab in DevTools
3. Authentication token valid

## Development

### Adding New Component

```typescript
// 1. Create component
// components/NewComponent.tsx

export function NewComponent() {
  return <div>New Component</div>
}

// 2. Import in App.tsx
import { NewComponent } from './components/NewComponent'

// 3. Use in render
<NewComponent />
```

### Adding New Command

```typescript
// In CommandPalette.tsx
commands.push({
  id: 'new-command',
  label: 'New Command',
  icon: 'icon-name',
  command: '/new',
  action: () => {
    // Your action here
  },
  shortcut: '⌘N',
})
```

### State Management

```typescript
// In store/factoryStore.ts
const useFactoryStore = create((set) => ({
  newState: null,
  setNewState: (value) => set({ newState: value }),
}))
```

## Contributing

See main CONTRIBUTING.md for guidelines.

## License

MIT

---

**Built with ❤️ for Botskis**

Questions? support@botskis.com
