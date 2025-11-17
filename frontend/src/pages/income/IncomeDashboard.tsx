import React, { useState, useEffect } from 'react';

// ============================================================================
// TYPES
// ============================================================================

interface IncomeStats {
  total_earnings_nok: number;
  earnings_today: number;
  earnings_this_week: number;
  earnings_this_month: number;
  by_bot_type: { [key: string]: number };
  by_platform: { [key: string]: number };
  total_jobs_completed: number;
  average_per_job: number;
  best_performing_bot: string;
  hourly_rate_estimate: number;
}

interface Transaction {
  id: number;
  bot_type: string;
  platform: string;
  job_title: string;
  amount_nok: number;
  status: string;
  earned_at: string;
}

interface BotStatus {
  bot_type: string;
  status: 'running' | 'stopped' | 'paused';
  jobs_today: number;
  earnings_today: number;
  last_job_at: string;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const IncomeDashboard: React.FC = () => {
  const [stats, setStats] = useState<IncomeStats | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [botStatuses, setBotStatuses] = useState<BotStatus[]>([]);
  const [forecast, setForecast] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      // In production, replace with actual API calls
      const response = await fetch('/api/v1/income/stats');
      const data = await response.json();

      setStats(data.stats);
      setTransactions(data.recent_transactions);
      setBotStatuses(data.bot_statuses);
      setForecast(data.monthly_forecast);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching income data:', error);

      // Mock data for demo
      setStats({
        total_earnings_nok: 5420,
        earnings_today: 320,
        earnings_this_week: 1840,
        earnings_this_month: 5420,
        by_bot_type: {
          freelance: 2400,
          testing: 680,
          survey: 540,
          writing: 1800
        },
        by_platform: {
          upwork: 1800,
          freelancer: 600,
          usertesting: 480,
          testbirds: 200,
          swagbucks: 340,
          ysense: 200,
          textbroker: 1200,
          iwriter: 600
        },
        total_jobs_completed: 78,
        average_per_job: 69.49,
        best_performing_bot: 'freelance',
        hourly_rate_estimate: 226.67
      });

      setTransactions([
        {
          id: 1,
          bot_type: 'freelance',
          platform: 'upwork',
          job_title: 'Write 10 blog articles about AI',
          amount_nok: 800,
          status: 'paid',
          earned_at: new Date().toISOString()
        },
        {
          id: 2,
          bot_type: 'testing',
          platform: 'usertesting',
          job_title: 'E-commerce usability test',
          amount_nok: 25,
          status: 'completed',
          earned_at: new Date(Date.now() - 1800000).toISOString()
        },
        {
          id: 3,
          bot_type: 'survey',
          platform: 'swagbucks',
          job_title: 'Consumer shopping habits survey',
          amount_nok: 8,
          status: 'paid',
          earned_at: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: 4,
          bot_type: 'writing',
          platform: 'textbroker',
          job_title: 'Guide to healthy eating on budget',
          amount_nok: 70,
          status: 'completed',
          earned_at: new Date(Date.now() - 7200000).toISOString()
        }
      ]);

      setBotStatuses([
        {
          bot_type: 'freelance',
          status: 'running',
          jobs_today: 3,
          earnings_today: 180,
          last_job_at: new Date(Date.now() - 900000).toISOString()
        },
        {
          bot_type: 'testing',
          status: 'running',
          jobs_today: 8,
          earnings_today: 80,
          last_job_at: new Date(Date.now() - 600000).toISOString()
        },
        {
          bot_type: 'survey',
          status: 'running',
          jobs_today: 12,
          earnings_today: 36,
          last_job_at: new Date(Date.now() - 300000).toISOString()
        },
        {
          bot_type: 'writing',
          status: 'paused',
          jobs_today: 1,
          earnings_today: 50,
          last_job_at: new Date(Date.now() - 14400000).toISOString()
        }
      ]);

      setForecast(12450);
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading income data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            💰 Income Dashboard
          </h1>
          <p className="text-gray-600">
            Real-time earnings from your autonomous income bots
          </p>
        </div>

        {/* Top Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Earnings"
            value={`${stats.total_earnings_nok.toLocaleString()} NOK`}
            icon="💎"
            color="blue"
          />
          <StatsCard
            title="Today"
            value={`${stats.earnings_today.toLocaleString()} NOK`}
            icon="📅"
            color="green"
          />
          <StatsCard
            title="This Week"
            value={`${stats.earnings_this_week.toLocaleString()} NOK`}
            icon="📊"
            color="purple"
          />
          <StatsCard
            title="This Month"
            value={`${stats.earnings_this_month.toLocaleString()} NOK`}
            icon="📈"
            color="orange"
          />
        </div>

        {/* Earnings by Bot Type */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Earnings by Bot Type</h2>
            <div className="space-y-3">
              {Object.entries(stats.by_bot_type).map(([bot, amount]) => (
                <BotTypeBar key={bot} bot={bot} amount={amount} total={stats.total_earnings_nok} />
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Performance Metrics</h2>
            <div className="space-y-4">
              <MetricRow label="Jobs Completed" value={stats.total_jobs_completed} />
              <MetricRow label="Average per Job" value={`${stats.average_per_job.toFixed(2)} NOK`} />
              <MetricRow label="Hourly Rate" value={`${stats.hourly_rate_estimate.toFixed(2)} NOK/hr`} />
              <MetricRow label="Best Bot" value={stats.best_performing_bot} />
              <MetricRow label="Monthly Forecast" value={`${forecast.toLocaleString()} NOK`} />
            </div>
          </div>
        </div>

        {/* Bot Status */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Bot Status (Live)</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {botStatuses.map(bot => (
              <BotStatusCard key={bot.bot_type} bot={bot} />
            ))}
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4">Recent Transactions</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Job</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bot</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Platform</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {transactions.map(tx => (
                  <TransactionRow key={tx.id} transaction={tx} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

interface StatsCardProps {
  title: string;
  value: string;
  icon: string;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200',
    green: 'bg-green-50 border-green-200',
    purple: 'bg-purple-50 border-purple-200',
    orange: 'bg-orange-50 border-orange-200'
  };

  return (
    <div className={`${colorClasses[color]} border-2 rounded-lg p-6`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-600 text-sm font-medium">{title}</span>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className="text-2xl font-bold text-gray-900">{value}</div>
    </div>
  );
};

interface BotTypeBarProps {
  bot: string;
  amount: number;
  total: number;
}

const BotTypeBar: React.FC<BotTypeBarProps> = ({ bot, amount, total }) => {
  const percentage = (amount / total) * 100;

  const botIcons: { [key: string]: string } = {
    freelance: '💼',
    testing: '🧪',
    survey: '📋',
    writing: '✍️'
  };

  const botColors: { [key: string]: string } = {
    freelance: 'bg-blue-500',
    testing: 'bg-green-500',
    survey: 'bg-purple-500',
    writing: 'bg-orange-500'
  };

  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium capitalize flex items-center gap-2">
          <span>{botIcons[bot]}</span>
          {bot}
        </span>
        <span className="text-sm font-medium">{amount.toLocaleString()} NOK</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`${botColors[bot]} h-2 rounded-full transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

interface MetricRowProps {
  label: string;
  value: string | number;
}

const MetricRow: React.FC<MetricRowProps> = ({ label, value }) => (
  <div className="flex justify-between items-center">
    <span className="text-gray-600">{label}</span>
    <span className="font-semibold text-gray-900">{value}</span>
  </div>
);

interface BotStatusCardProps {
  bot: BotStatus;
}

const BotStatusCard: React.FC<BotStatusCardProps> = ({ bot }) => {
  const statusColors = {
    running: 'bg-green-100 text-green-800 border-green-300',
    stopped: 'bg-red-100 text-red-800 border-red-300',
    paused: 'bg-yellow-100 text-yellow-800 border-yellow-300'
  };

  const botIcons: { [key: string]: string } = {
    freelance: '💼',
    testing: '🧪',
    survey: '📋',
    writing: '✍️'
  };

  const timeAgo = (date: string) => {
    const seconds = Math.floor((new Date().getTime() - new Date(date).getTime()) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    return `${Math.floor(seconds / 3600)}h ago`;
  };

  return (
    <div className="border-2 border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-2xl">{botIcons[bot.bot_type]}</span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${statusColors[bot.status]}`}>
          {bot.status}
        </span>
      </div>
      <h3 className="font-semibold capitalize mb-2">{bot.bot_type} Bot</h3>
      <div className="text-sm text-gray-600 space-y-1">
        <div>Jobs today: <span className="font-medium">{bot.jobs_today}</span></div>
        <div>Earned: <span className="font-medium">{bot.earnings_today} NOK</span></div>
        <div>Last job: <span className="font-medium">{timeAgo(bot.last_job_at)}</span></div>
      </div>
    </div>
  );
};

interface TransactionRowProps {
  transaction: Transaction;
}

const TransactionRow: React.FC<TransactionRowProps> = ({ transaction }) => {
  const timeAgo = (date: string) => {
    const seconds = Math.floor((new Date().getTime() - new Date(date).getTime()) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    return `${Math.floor(seconds / 3600)}h ago`;
  };

  const statusColors = {
    paid: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    pending: 'bg-yellow-100 text-yellow-800'
  };

  return (
    <tr>
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{transaction.job_title}</td>
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 capitalize">{transaction.bot_type}</td>
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{transaction.platform}</td>
      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
        {transaction.amount_nok} NOK
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[transaction.status as keyof typeof statusColors]}`}>
          {transaction.status}
        </span>
      </td>
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{timeAgo(transaction.earned_at)}</td>
    </tr>
  );
};

export default IncomeDashboard;
