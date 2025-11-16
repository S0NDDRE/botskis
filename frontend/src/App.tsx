import { Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './stores/authStore'

// Layouts
import DashboardLayout from './components/layouts/DashboardLayout'
import AuthLayout from './components/layouts/AuthLayout'

// Auth Pages
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'

// Dashboard Pages
import DashboardHome from './pages/dashboard/DashboardHome'

// Academy Pages
import AcademyDashboard from './pages/academy/AcademyDashboard'
import CourseList from './pages/academy/CourseList'
import CoursePlayer from './pages/academy/CoursePlayer'
import LearningPaths from './pages/academy/LearningPaths'
import MyCourses from './pages/academy/MyCourses'
import Certificates from './pages/academy/Certificates'

// AI Agent Pages
import AIAgentList from './pages/agents/AIAgentList'
import AIAgentCreate from './pages/agents/AIAgentCreate'
import AIAgentDetail from './pages/agents/AIAgentDetail'

// Voice AI Pages
import VoiceAIDashboard from './pages/voice/VoiceAIDashboard'
import VoiceAgents from './pages/voice/VoiceAgents'
import CallHistory from './pages/voice/CallHistory'

// Meta-AI Guardian Pages
import GuardianDashboard from './pages/guardian/GuardianDashboard'
import ApprovalQueue from './pages/guardian/ApprovalQueue'
import OptimizationHistory from './pages/guardian/OptimizationHistory'

// Analytics Pages
import Analytics from './pages/analytics/Analytics'
import Reports from './pages/analytics/Reports'

// Marketplace
import Marketplace from './pages/marketplace/Marketplace'
import MarketplaceDetail from './pages/marketplace/MarketplaceDetail'

// Settings Pages
import Settings from './pages/settings/Settings'
import TeamSettings from './pages/settings/TeamSettings'
import BillingSettings from './pages/settings/BillingSettings'
import Webhooks from './pages/settings/Webhooks'

// Protected Route Component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function App() {
  return (
    <>
      <Routes>
        {/* Auth Routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>

        {/* Dashboard Routes */}
        <Route
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          {/* Home */}
          <Route path="/" element={<DashboardHome />} />
          
          {/* Academy */}
          <Route path="/academy" element={<AcademyDashboard />} />
          <Route path="/academy/courses" element={<CourseList />} />
          <Route path="/academy/courses/:courseId" element={<CoursePlayer />} />
          <Route path="/academy/paths" element={<LearningPaths />} />
          <Route path="/academy/my-courses" element={<MyCourses />} />
          <Route path="/academy/certificates" element={<Certificates />} />
          
          {/* AI Agents */}
          <Route path="/agents" element={<AIAgentList />} />
          <Route path="/agents/create" element={<AIAgentCreate />} />
          <Route path="/agents/:agentId" element={<AIAgentDetail />} />
          
          {/* Voice AI */}
          <Route path="/voice" element={<VoiceAIDashboard />} />
          <Route path="/voice/agents" element={<VoiceAgents />} />
          <Route path="/voice/calls" element={<CallHistory />} />
          
          {/* Meta-AI Guardian */}
          <Route path="/guardian" element={<GuardianDashboard />} />
          <Route path="/guardian/approvals" element={<ApprovalQueue />} />
          <Route path="/guardian/history" element={<OptimizationHistory />} />
          
          {/* Analytics */}
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/reports" element={<Reports />} />
          
          {/* Marketplace */}
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/marketplace/:agentId" element={<MarketplaceDetail />} />
          
          {/* Settings */}
          <Route path="/settings" element={<Settings />} />
          <Route path="/settings/team" element={<TeamSettings />} />
          <Route path="/settings/billing" element={<BillingSettings />} />
          <Route path="/settings/webhooks" element={<Webhooks />} />
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          className: 'dark:bg-gray-800 dark:text-white',
        }}
      />
    </>
  )
}

export default App
