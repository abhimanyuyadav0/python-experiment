'use client';
import { useAuth } from "@/contexts/AuthContext";

const UserDashboardPage = () => {
  const { user } = useAuth();
  return (
    <div>
      <h1>User Dashboard</h1>
      <p>Welcome to your user dashboard</p>
      <p>
        Welcome back, {user?.name}. Here's what's happening with your system
        today.
      </p>
      <div className="flex flex-col gap-2">
     
      </div>
    </div>
  );
};

export default UserDashboardPage;
