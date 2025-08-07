'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function AdminAnalyticsPage() {
  const { user } = useAuth();

  const analyticsData = [
    { name: 'Total Users', value: '1,234', change: '+12.3%', changeType: 'positive' },
    { name: 'Active Sessions', value: '89', change: '-5.2%', changeType: 'negative' },
    { name: 'New Registrations', value: '45', change: '+8.1%', changeType: 'positive' },
    { name: 'System Uptime', value: '99.9%', change: '+0.1%', changeType: 'positive' },
  ];

  const topUsers = [
    { name: 'John Doe', email: 'john@example.com', role: 'admin', lastActive: '2 hours ago' },
    { name: 'Jane Smith', email: 'jane@example.com', role: 'tenant', lastActive: '4 hours ago' },
    { name: 'Bob Johnson', email: 'bob@example.com', role: 'user', lastActive: '1 day ago' },
    { name: 'Alice Brown', email: 'alice@example.com', role: 'tenant', lastActive: '2 days ago' },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Analytics Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700">
          View system analytics and user activity metrics.
        </p>
      </div>

      {/* Analytics Overview */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {analyticsData.map((item) => (
          <div key={item.name} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{item.name}</dt>
                    <dd className="text-lg font-medium text-gray-900">{item.value}</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm">
                <span className={`font-medium ${
                  item.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {item.change}
                </span>
                <span className="text-gray-500"> from last week</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Chart Placeholder */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">User Growth</h3>
            <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="mt-2 text-sm text-gray-500">Chart visualization would go here</p>
                <p className="text-xs text-gray-400">Integration with charting library required</p>
              </div>
            </div>
          </div>
        </div>

        {/* Top Active Users */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Most Active Users</h3>
            <div className="flow-root">
              <ul className="-mb-8">
                {topUsers.map((userItem, userIdx) => (
                  <li key={userItem.email}>
                    <div className="relative pb-8">
                      {userIdx !== topUsers.length - 1 ? (
                        <span
                          className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                          aria-hidden="true"
                        />
                      ) : null}
                      <div className="relative flex space-x-3">
                        <div>
                          <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                            <span className="text-white text-sm font-medium">
                              {userItem.name.charAt(0).toUpperCase()}
                            </span>
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                          <div>
                            <p className="text-sm text-gray-500">
                              <span className="font-medium text-gray-900">{userItem.name}</span>
                              <span className="text-gray-400"> • {userItem.email}</span>
                            </p>
                            <p className="text-xs text-gray-400">
                              Role: <span className="font-medium">{userItem.role}</span>
                            </p>
                          </div>
                          <div className="text-right text-sm whitespace-nowrap text-gray-500">
                            <time dateTime={userItem.lastActive}>{userItem.lastActive}</time>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Analytics Sections */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Role Distribution</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">Users</span>
                <span className="text-sm text-gray-500">1,156 (93.7%)</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '93.7%' }}></div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">Tenants</span>
                <span className="text-sm text-gray-500">45 (3.6%)</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-green-600 h-2 rounded-full" style={{ width: '3.6%' }}></div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">Admins</span>
                <span className="text-sm text-gray-500">33 (2.7%)</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-red-600 h-2 rounded-full" style={{ width: '2.7%' }}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">System Performance</h3>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900">CPU Usage</span>
                  <span className="text-sm text-gray-500">23%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div className="bg-green-600 h-2 rounded-full" style={{ width: '23%' }}></div>
                </div>
              </div>
              
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900">Memory Usage</span>
                  <span className="text-sm text-gray-500">67%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div className="bg-yellow-600 h-2 rounded-full" style={{ width: '67%' }}></div>
                </div>
              </div>
              
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900">Disk Usage</span>
                  <span className="text-sm text-gray-500">45%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '45%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 