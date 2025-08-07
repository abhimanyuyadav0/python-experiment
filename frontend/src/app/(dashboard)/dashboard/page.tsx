'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function DashboardPage() {
  const { user, isAdmin, isTenant, isUser } = useAuth();

  const getStats = () => {
    if (isAdmin()) {
      return [
        { name: 'Total Users', value: '1,234', change: '+12.3%', changeType: 'positive' },
        { name: 'Total Tenants', value: '45', change: '+8.1%', changeType: 'positive' },
        { name: 'Active Admins', value: '3', change: '+0%', changeType: 'positive' },
        { name: 'System Health', value: '98%', change: '+2%', changeType: 'positive' },
      ];
    } else if (isTenant()) {
      return [
        { name: 'Total Users', value: '156', change: '+12%', changeType: 'positive' },
        { name: 'Active Projects', value: '8', change: '+2', changeType: 'positive' },
        { name: 'Storage Used', value: '2.4 GB', change: '+15%', changeType: 'positive' },
        { name: 'API Calls', value: '12.5K', change: '+8.3%', changeType: 'positive' },
      ];
    } else {
      return [
        { name: 'My Projects', value: '3', change: '+1', changeType: 'positive' },
        { name: 'Tasks Completed', value: '24', change: '+6', changeType: 'positive' },
        { name: 'Storage Used', value: '1.2 GB', change: '+8%', changeType: 'positive' },
        { name: 'Last Login', value: '2h ago', change: '', changeType: 'positive' },
      ];
    }
  };

  const stats = getStats();

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          Welcome back, {user?.name}!
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Here's what's happening with your account today.
        </p>
        <div className="mt-2">
          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
            isAdmin() ? 'bg-red-100 text-red-800' :
            isTenant() ? 'bg-green-100 text-green-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {user?.role?.toUpperCase()} Role
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-indigo-500 rounded-md flex items-center justify-center">
                    <svg
                      className="w-5 h-5 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                      />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        {stat.value}
                      </div>
                      <div
                        className={`ml-2 flex items-baseline text-sm font-semibold ${
                          stat.changeType === 'positive'
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {stat.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Recent Activity
          </h3>
          <div className="flow-root">
            <ul className="-mb-8">
              {(() => {
                if (isAdmin()) {
                  return [
                    {
                      id: 1,
                      type: 'user_created',
                      content: 'New admin user "admin@company.com" was created',
                      date: '2 hours ago',
                    },
                    {
                      id: 2,
                      type: 'tenant_created',
                      content: 'New tenant "Acme Corp" was created',
                      date: '4 hours ago',
                    },
                    {
                      id: 3,
                      type: 'role_updated',
                      content: 'User role updated for "john.doe@acme.com"',
                      date: '1 day ago',
                    },
                    {
                      id: 4,
                      type: 'system_update',
                      content: 'System maintenance completed successfully',
                      date: '2 days ago',
                    },
                  ];
                } else if (isTenant()) {
                  return [
                    {
                      id: 1,
                      type: 'user_created',
                      content: 'New user "jane.smith@company.com" was added',
                      date: '2 hours ago',
                    },
                    {
                      id: 2,
                      type: 'project_created',
                      content: 'New project "E-commerce Platform" was created',
                      date: '4 hours ago',
                    },
                    {
                      id: 3,
                      type: 'user_login',
                      content: 'User "john.doe@company.com" logged in',
                      date: '1 day ago',
                    },
                    {
                      id: 4,
                      type: 'project_updated',
                      content: 'Project "Mobile App" settings updated',
                      date: '2 days ago',
                    },
                  ];
                } else {
                  return [
                    {
                      id: 1,
                      type: 'task_completed',
                      content: 'Task "Update documentation" was completed',
                      date: '2 hours ago',
                    },
                    {
                      id: 2,
                      type: 'project_joined',
                      content: 'Joined project "E-commerce Platform"',
                      date: '4 hours ago',
                    },
                    {
                      id: 3,
                      type: 'profile_updated',
                      content: 'Profile information was updated',
                      date: '1 day ago',
                    },
                    {
                      id: 4,
                      type: 'login',
                      content: 'Successfully logged in to the system',
                      date: '2 days ago',
                    },
                  ];
                }
              })().map((activity, activityIdx) => (
                <li key={activity.id}>
                  <div className="relative pb-8">
                    {activityIdx !== 3 ? (
                      <span
                        className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    ) : null}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className="h-8 w-8 rounded-full bg-indigo-500 flex items-center justify-center ring-8 ring-white">
                          <svg
                            className="w-5 h-5 text-white"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                            />
                          </svg>
                        </span>
                      </div>
                      <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p className="text-sm text-gray-500">
                            {activity.content}
                          </p>
                        </div>
                        <div className="text-right text-sm whitespace-nowrap text-gray-500">
                          <time dateTime={activity.date}>{activity.date}</time>
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
  );
} 