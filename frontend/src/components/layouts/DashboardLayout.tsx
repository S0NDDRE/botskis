import { Outlet } from 'react-router-dom'
import { useUIStore } from '../../stores/uiStore'
import Sidebar from '../common/Sidebar'
import Header from '../common/Header'
import NotificationCenter from '../common/NotificationCenter'

export default function DashboardLayout() {
  const { sidebarOpen } = useUIStore()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar />

      <div
        className={`transition-all duration-300 ${sidebarOpen ? 'lg:ml-64' : 'lg:ml-20'}`}
      >
        <Header />

        <main className="p-6">
          <Outlet />
        </main>
      </div>

      <NotificationCenter />
    </div>
  )
}
