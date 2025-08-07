'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function AdminSettingsPage() {
  const { user } = useAuth();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">System Settings</h1>
        <p className="mt-2 text-sm text-gray-700">
          Configure system-wide settings and preferences.
        </p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">General Settings</h3>
          
          <div className="space-y-6">
            <div>
              <label htmlFor="site-name" className="block text-sm font-medium text-gray-700">
                Site Name
              </label>
              <input
                type="text"
                name="site-name"
                id="site-name"
                defaultValue="Admin Panel"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="site-description" className="block text-sm font-medium text-gray-700">
                Site Description
              </label>
              <textarea
                name="site-description"
                id="site-description"
                rows={3}
                defaultValue="Multi-tenant application with role-based access control"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="timezone" className="block text-sm font-medium text-gray-700">
                Default Timezone
              </label>
              <select
                name="timezone"
                id="timezone"
                defaultValue="UTC"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="UTC">UTC</option>
                <option value="EST">Eastern Standard Time</option>
                <option value="PST">Pacific Standard Time</option>
                <option value="GMT">Greenwich Mean Time</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                id="maintenance-mode"
                name="maintenance-mode"
                type="checkbox"
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="maintenance-mode" className="ml-2 block text-sm text-gray-900">
                Enable Maintenance Mode
              </label>
            </div>

            <div className="flex items-center">
              <input
                id="debug-mode"
                name="debug-mode"
                type="checkbox"
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="debug-mode" className="ml-2 block text-sm text-gray-900">
                Enable Debug Mode
              </label>
            </div>
          </div>

          <div className="mt-6">
            <button
              type="button"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Save Settings
            </button>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Security Settings</h3>
          
          <div className="space-y-6">
            <div>
              <label htmlFor="session-timeout" className="block text-sm font-medium text-gray-700">
                Session Timeout (minutes)
              </label>
              <input
                type="number"
                name="session-timeout"
                id="session-timeout"
                defaultValue="30"
                min="5"
                max="480"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="max-login-attempts" className="block text-sm font-medium text-gray-700">
                Maximum Login Attempts
              </label>
              <input
                type="number"
                name="max-login-attempts"
                id="max-login-attempts"
                defaultValue="5"
                min="3"
                max="10"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div className="flex items-center">
              <input
                id="two-factor-auth"
                name="two-factor-auth"
                type="checkbox"
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="two-factor-auth" className="ml-2 block text-sm text-gray-900">
                Require Two-Factor Authentication for Admins
              </label>
            </div>
          </div>

          <div className="mt-6">
            <button
              type="button"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Save Security Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 