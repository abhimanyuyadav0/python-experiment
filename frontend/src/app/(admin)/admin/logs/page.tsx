'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function AdminLogsPage() {
  const { user } = useAuth();

  const logEntries = [
    {
      id: 1,
      timestamp: '2024-01-15 14:30:25',
      level: 'INFO',
      message: 'User john@example.com logged in successfully',
      source: 'auth',
      userId: 'john@example.com'
    },
    {
      id: 2,
      timestamp: '2024-01-15 14:28:15',
      level: 'WARNING',
      message: 'Failed login attempt for user unknown@example.com',
      source: 'auth',
      userId: 'unknown@example.com'
    },
    {
      id: 3,
      timestamp: '2024-01-15 14:25:42',
      level: 'INFO',
      message: 'User role updated: jane@example.com -> admin',
      source: 'user_management',
      userId: 'jane@example.com'
    },
    {
      id: 4,
      timestamp: '2024-01-15 14:22:18',
      level: 'ERROR',
      message: 'Database connection timeout',
      source: 'database',
      userId: null
    },
    {
      id: 5,
      timestamp: '2024-01-15 14:20:33',
      level: 'INFO',
      message: 'New user registered: bob@example.com',
      source: 'registration',
      userId: 'bob@example.com'
    },
    {
      id: 6,
      timestamp: '2024-01-15 14:18:55',
      level: 'INFO',
      message: 'System backup completed successfully',
      source: 'system',
      userId: null
    },
    {
      id: 7,
      timestamp: '2024-01-15 14:15:12',
      level: 'WARNING',
      message: 'High memory usage detected: 85%',
      source: 'monitoring',
      userId: null
    },
    {
      id: 8,
      timestamp: '2024-01-15 14:12:47',
      level: 'INFO',
      message: 'API rate limit exceeded for IP 192.168.1.100',
      source: 'api',
      userId: null
    }
  ];

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR':
        return 'bg-red-100 text-red-800';
      case 'WARNING':
        return 'bg-yellow-100 text-yellow-800';
      case 'INFO':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'auth':
        return 'bg-purple-100 text-purple-800';
      case 'user_management':
        return 'bg-green-100 text-green-800';
      case 'database':
        return 'bg-red-100 text-red-800';
      case 'registration':
        return 'bg-blue-100 text-blue-800';
      case 'system':
        return 'bg-gray-100 text-gray-800';
      case 'monitoring':
        return 'bg-yellow-100 text-yellow-800';
      case 'api':
        return 'bg-indigo-100 text-indigo-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">System Logs</h1>
        <p className="mt-2 text-sm text-gray-700">
          View system logs and activity history.
        </p>
      </div>

      {/* Log Filters */}
      <div className="bg-white shadow rounded-lg mb-8">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Filters</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label htmlFor="log-level" className="block text-sm font-medium text-gray-700">
                Log Level
              </label>
              <select
                id="log-level"
                name="log-level"
                defaultValue="all"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="all">All Levels</option>
                <option value="ERROR">Error</option>
                <option value="WARNING">Warning</option>
                <option value="INFO">Info</option>
              </select>
            </div>

            <div>
              <label htmlFor="log-source" className="block text-sm font-medium text-gray-700">
                Source
              </label>
              <select
                id="log-source"
                name="log-source"
                defaultValue="all"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="all">All Sources</option>
                <option value="auth">Authentication</option>
                <option value="user_management">User Management</option>
                <option value="database">Database</option>
                <option value="system">System</option>
                <option value="api">API</option>
              </select>
            </div>

            <div>
              <label htmlFor="date-from" className="block text-sm font-medium text-gray-700">
                From Date
              </label>
              <input
                type="datetime-local"
                id="date-from"
                name="date-from"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="date-to" className="block text-sm font-medium text-gray-700">
                To Date
              </label>
              <input
                type="datetime-local"
                id="date-to"
                name="date-to"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="mt-4 flex space-x-3">
            <button
              type="button"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Apply Filters
            </button>
            <button
              type="button"
              className="bg-gray-300 hover:bg-gray-400 text-gray-700 px-4 py-2 rounded-md text-sm font-medium"
            >
              Clear Filters
            </button>
            <button
              type="button"
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Export Logs
            </button>
          </div>
        </div>
      </div>

      {/* Log Entries */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Recent Log Entries</h3>
            <span className="text-sm text-gray-500">Showing {logEntries.length} entries</span>
          </div>

          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Level
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Message
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {logEntries.map((entry) => (
                  <tr key={entry.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {entry.timestamp}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getLevelColor(entry.level)}`}>
                        {entry.level}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSourceColor(entry.source)}`}>
                        {entry.source.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {entry.message}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {entry.userId || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="mt-6 flex items-center justify-between">
            <div className="flex-1 flex justify-between sm:hidden">
              <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Previous
              </button>
              <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing <span className="font-medium">1</span> to <span className="font-medium">{logEntries.length}</span> of{' '}
                  <span className="font-medium">{logEntries.length}</span> results
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <button className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Previous
                  </button>
                  <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
                    1
                  </button>
                  <button className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Next
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 