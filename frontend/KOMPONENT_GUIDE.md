# 📦 NYE KOMPONENTER - Bruksveiledning
**4 nye komponenter for forbedret brukeropplevelse**

---

## ✅ FERDIGSTILT (100%)

### 1. Live Chat Widget 💬
**Fil:** `frontend/src/components/LiveChatWidget.tsx`

**Beskrivelse:**
Floating chat widget for kundesupport med WebSocket real-time messaging.

**Features:**
- Floating chat button (bottom-right)
- Minimiser/maksimer funksjon
- Unread notification badge
- Real-time messaging (WebSocket)
- "Agent typing" indikator
- Auto-scroll til nye meldinger
- Connection status
- Message timestamps

**Bruk:**
```tsx
import { LiveChatWidget } from './components/LiveChatWidget';

function App() {
  return (
    <div>
      <YourContent />
      <LiveChatWidget apiUrl="http://localhost:8000" />
    </div>
  );
}
```

**Props:**
- `apiUrl` (optional): Backend URL (default: http://localhost:8000)

**Backend:**
- WebSocket endepunkt: `/ws/chat`
- Backend allerede implementert: `src/support/live_chat.py`

---

### 2. Notification Center 🔔
**Fil:** `frontend/src/components/NotificationCenter.tsx`

**Beskrivelse:**
Notification bell med dropdown for in-app varsler.

**Features:**
- Notification bell icon
- Unread count badge
- Dropdown med alle varsler
- 4 typer: info, success, warning, error
- Mark as read (enkelt eller alle)
- Delete notifications
- Clear all
- Action links (se detaljer)
- Auto-timestamp (akkurat nå, 5 min siden, etc.)
- Click outside to close

**Bruk:**
```tsx
import { NotificationCenter } from './components/NotificationCenter';

// I header/navbar:
function Header() {
  return (
    <header>
      <div className="flex items-center space-x-4">
        <NotificationCenter />
        <UserMenu />
      </div>
    </header>
  );
}
```

**Props:**
- Ingen props (standalone komponent)

**Backend:**
- Kan kobles til WebSocket for real-time updates
- Eller polling hver 30s

---

### 3. Onboarding Tour 🎯
**Fil:** `frontend/src/components/OnboardingTour.tsx`

**Beskrivelse:**
Step-by-step guided tour for nye brukere.

**Features:**
- Initial welcome modal
- Highlight UI elements
- Step-by-step guide (6 steg)
- Progress bar
- Skip/Back/Next navigation
- Auto-scroll to elements
- Local storage tracking (vises kun én gang)
- Custom actions per step
- Overlay med fokus på target element

**Bruk:**
```tsx
import { OnboardingTour } from './components/OnboardingTour';

function Dashboard() {
  const isNewUser = true; // Check from user profile

  return (
    <div>
      <OnboardingTour
        isNewUser={isNewUser}
        onComplete={() => console.log('Tour completed!')}
      />

      {/* Add data-tour attributes to elements */}
      <div data-tour="dashboard">Dashboard</div>
      <div data-tour="agents">Agents</div>
      <div data-tour="marketplace">Marketplace</div>
      <div data-tour="create-agent">
        <button>Create Agent</button>
      </div>
    </div>
  );
}
```

**Props:**
- `isNewUser` (boolean): Vis tour automatisk for nye brukere
- `onComplete` (function): Callback når tour er ferdig

**Data Attributes:**
Legg til `data-tour="id"` på elementer du vil highlighte:
```tsx
<button data-tour="create-agent">Create</button>
<nav data-tour="dashboard">Dashboard</nav>
```

---

### 4. Advanced Logs Viewer 📊
**Fil:** `frontend/src/components/AdvancedLogsViewer.tsx`

**Beskrivelse:**
Avansert logs viewer med filter, søk og eksport.

**Features:**
- Real-time log streaming
- 5 log levels (debug, info, warning, error, critical)
- Filter by level
- Search (søk i message og source)
- Time range filter (15m, 1h, 24h, 7d, 30d)
- Auto-refresh (5s interval)
- Export logs (JSON eller CSV)
- Clear all logs
- Click log for full details
- Stack trace viewer (for errors)
- Metadata viewer
- Icons per log level

**Bruk:**
```tsx
import { AdvancedLogsViewer } from './components/AdvancedLogsViewer';

function LogsPage() {
  return (
    <div>
      <h1>Agent Logs</h1>
      <AdvancedLogsViewer agentId="agent-123" />
    </div>
  );
}
```

**Props:**
- `agentId` (optional): Filter logs for specific agent
- `source` (optional): Filter logs by source

**API Integration:**
Backend endpoint: `/api/v1/logs`
```typescript
// Fetch logs
GET /api/v1/logs?level=error&timeRange=1h&agentId=agent-123
```

---

## 🎨 STYLING

Alle komponenter bruker **Tailwind CSS** og følger samme design system:

**Farger:**
- Primary: `blue-600`
- Success: `green-600`
- Warning: `yellow-600`
- Error: `red-600`
- Info: `blue-600`

**Shadows:**
- Small: `shadow`
- Medium: `shadow-lg`
- Large: `shadow-2xl`

**Responsive:**
Alle komponenter er responsive og fungerer på mobil.

---

## 🔌 INTEGRASJON

### 1. Legg til i App.tsx (Main App)

```tsx
import { LiveChatWidget } from './components/LiveChatWidget';
import { OnboardingTour } from './components/OnboardingTour';

function App() {
  const user = useAuth(); // Hent bruker

  return (
    <Router>
      {/* Existing routes */}
      <Routes>...</Routes>

      {/* Global components */}
      <LiveChatWidget />
      <OnboardingTour isNewUser={user?.isNew} />
    </Router>
  );
}
```

### 2. Legg til i Header/Navbar

```tsx
import { NotificationCenter } from './components/NotificationCenter';

function Header() {
  return (
    <header className="flex items-center justify-between p-4">
      <Logo />
      <div className="flex items-center space-x-4">
        <NotificationCenter />
        <UserMenu />
      </div>
    </header>
  );
}
```

### 3. Logs Viewer i Agent Details

```tsx
import { AdvancedLogsViewer } from './components/AdvancedLogsViewer';

function AgentDetailPage({ agentId }) {
  return (
    <div>
      <Tabs>
        <Tab label="Overview">...</Tab>
        <Tab label="Logs">
          <AdvancedLogsViewer agentId={agentId} />
        </Tab>
      </Tabs>
    </div>
  );
}
```

---

## 📱 RESPONSIVITET

Alle komponenter er responsive:

**Mobile (< 640px):**
- Live Chat: Full width på små skjermer
- Notifications: Dropdown justeres for small screen
- Onboarding: Tour tooltip justeres
- Logs: Table blir scrollable

**Tablet (640px - 1024px):**
- Alle komponenter skaleres pent

**Desktop (> 1024px):**
- Full funksjonalitet

---

## 🧪 TESTING

Test komponentene:

```bash
# Start frontend
npm run dev

# Test Live Chat
# 1. Åpne http://localhost:5173
# 2. Se chat button nederst til høyre
# 3. Klikk og send melding

# Test Notifications
# 1. Se notification bell i header
# 2. Klikk for å se dropdown
# 3. Test mark as read

# Test Onboarding
# 1. Clear localStorage: localStorage.clear()
# 2. Refresh page
# 3. Se welcome modal
# 4. Start tour

# Test Logs
# 1. Gå til /logs eller agent details
# 2. Se logs liste
# 3. Test filter, search, export
```

---

## ⚙️ KONFIGURASJON

### Live Chat WebSocket
Konfig backend URL:
```tsx
<LiveChatWidget apiUrl={process.env.REACT_APP_API_URL} />
```

### Notifications Polling
Endre polling interval:
```tsx
// I NotificationCenter.tsx
const interval = setInterval(() => {
  fetchNewNotifications();
}, 30000); // 30 sekunder
```

### Onboarding Steps
Customize tour steps i `OnboardingTour.tsx`:
```tsx
const tourSteps: TourStep[] = [
  {
    id: 'welcome',
    title: 'Velkommen!',
    description: 'La oss starte...'
  },
  // Legg til dine egne steps
];
```

### Logs Auto-refresh
Endre refresh interval:
```tsx
// I AdvancedLogsViewer.tsx
const interval = setInterval(() => {
  fetchLogs();
}, 5000); // 5 sekunder
```

---

## 🐛 TROUBLESHOOTING

**Live Chat ikke kobler til:**
- Sjekk at backend WebSocket kjører
- Sjekk apiUrl er korrekt
- Sjekk CORS settings

**Notifications vises ikke:**
- Sjekk at komponenten er i header
- Sjekk z-index (må være > 40)

**Onboarding tour ikke starter:**
- Sjekk `isNewUser` prop
- Clear localStorage: `localStorage.clear()`
- Sjekk at data-tour attributes er riktige

**Logs laster ikke:**
- Sjekk API endpoint
- Sjekk console for errors
- Verify mock data loads first

---

## 📚 NESTE STEG

1. **Integrer komponentene:**
   - Legg til i App.tsx
   - Legg til i Header
   - Legg til i relevante sider

2. **Koble til backend:**
   - WebSocket for Live Chat
   - Notifications API
   - Logs API

3. **Tilpass design:**
   - Endre farger
   - Endre tekster
   - Legg til logo

4. **Test grundig:**
   - Test alle features
   - Test på mobil
   - Test med real data

---

## ✅ CHECKLIST

- [ ] Live Chat Widget integrert
- [ ] Notification Center i header
- [ ] Onboarding Tour konfigurert
- [ ] Logs Viewer i agent details
- [ ] WebSocket backend koblet til
- [ ] API endpoints konfigurert
- [ ] Testet på desktop
- [ ] Testet på mobil
- [ ] Custom styling aplikert
- [ ] Data-tour attributes lagt til

---

**Lykke til! 🚀**

**Mindframe AI - Forbedret Brukeropplevelse**
