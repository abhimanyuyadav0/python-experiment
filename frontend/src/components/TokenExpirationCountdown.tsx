'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface TokenData {
  token: string;
  expiresAt: number;
}

export default function TokenExpirationCountdown() {
  const [timeLeft, setTimeLeft] = useState<string>('');
  const { token } = useAuth();

  useEffect(() => {
    if (!token) {
      setTimeLeft('');
      return;
    }

    const updateCountdown = () => {
      const tokenDataStr = localStorage.getItem('tokenData');
      if (!tokenDataStr) {
        setTimeLeft('');
        return;
      }

      try {
        const tokenData: TokenData = JSON.parse(tokenDataStr);
        const now = Date.now();
        const timeRemaining = tokenData.expiresAt - now;

        // Debug logging
        console.log('Token Debug:', {
          expiresAt: tokenData.expiresAt,
          now: now,
          timeRemaining: timeRemaining,
          expiresAtDate: new Date(tokenData.expiresAt),
          nowDate: new Date(now)
        });

        if (timeRemaining <= 0) {
          setTimeLeft('Expired');
          return;
        }

        const minutes = Math.floor(timeRemaining / 60000);
        const seconds = Math.floor((timeRemaining % 60000) / 1000);
        setTimeLeft(`${minutes}:${seconds.toString().padStart(2, '0')}`);
      } catch (error) {
        console.error('Error parsing token data:', error);
        setTimeLeft('');
      }
    };

    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);

    return () => clearInterval(interval);
  }, [token]);

  if (!token || !timeLeft) {
    return null;
  }

  const isExpiringSoon = timeLeft !== 'Expired' && parseInt(timeLeft.split(':')[0]) < 1;

  return (
    <div className={`text-xs px-2 py-1 rounded ${
      isExpiringSoon 
        ? 'bg-red-100 text-red-800' 
        : 'bg-yellow-100 text-yellow-800'
    }`}>
      Token expires in: {timeLeft}
    </div>
  );
} 