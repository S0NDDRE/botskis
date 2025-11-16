import { Link } from 'react-router-dom'
import { User, Users, CreditCard, Webhook, Bell, Shield } from 'lucide-react'

export default function Settings() {
  const sections = [
    { name: 'Profile', icon: User, href: '/settings', description: 'Manage your account settings' },
    { name: 'Team', icon: Users, href: '/settings/team', description: 'Invite and manage team members' },
    { name: 'Billing', icon: CreditCard, href: '/settings/billing', description: 'Subscription and payment settings' },
    { name: 'Webhooks', icon: Webhook, href: '/settings/webhooks', description: 'Configure webhook integrations' },
    { name: 'Notifications', icon: Bell, href: '/settings/notifications', description: 'Notification preferences' },
    { name: 'Security', icon: Shield, href: '/settings/security', description: 'Security and privacy settings' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Manage your account and preferences
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sections.map((section) => (
          <Link
            key={section.name}
            to={section.href}
            className="card p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start gap-4">
              <div className="bg-primary-100 dark:bg-primary-900/30 p-3 rounded-lg">
                <section.icon className="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                  {section.name}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {section.description}
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
