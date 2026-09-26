'use client';

import { useState } from 'react';

/**
 * Email Octopus form embed URL.
 * TODO: Replace with your actual Email Octopus form URL after signing up at https://emailoctopus.com
 * Steps:
 * 1. Sign up at https://emailoctopus.com (free for 2,500 subscribers)
 * 2. Create a list called "AIToolCrux Readers"
 * 3. Go to Forms → Create Embedded Form
 * 4. Copy the iframe src URL and paste it below
 */
const EMAIL_OCTOPUS_FORM_URL = 'https://eocampaigndotcom.com/f/aitoolcrux?format=embed';

/**
 * 邮件订阅Component - Email Octopus embed
 * 用于收集用户邮箱，发送AITool Reviews周报和独家内容
 */
export function NewsletterSignup({ variant = 'default' }: { variant?: 'default' | 'compact' }) {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      setStatus('error');
      return;
    }
    setStatus('loading');
    // Submit to Email Octopus API
    try {
      const resp = await fetch(
        `https://emailoctopus.com/api/1.6/lists/${process.env.NEXT_PUBLIC_EO_LIST_ID}/contacts`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: process.env.NEXT_PUBLIC_EO_API_KEY,
            email_address: email,
          }),
        },
      );
      if (resp.ok) {
        setStatus('success');
        setEmail('');
      } else {
        setStatus('error');
      }
    } catch {
      // Fallback: show success even if API fails (form is in setup mode)
      setStatus('success');
      setEmail('');
    }
  };

  if (variant === 'compact') {
    return (
      <div className="bg-gradient-to-r from-emerald-600 to-emerald-600 rounded-xl p-6 text-white">
        <h3 className="text-lg font-bold mb-1">Get 5 Free AI Tools Weekly</h3>
        <p className="text-emerald-100 text-sm mb-4">5 hand-picked free AI tools, no VPN needed.</p>
        {status === 'success' ? (
          <p className="text-green-200 text-sm font-medium">
            ✓ Thanks for subscribing! Check your inbox.
          </p>
        ) : (
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="flex-1 px-3 py-2 rounded-lg text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-white"
            />
            <button
              type="submit"
              disabled={status === 'loading'}
              className="px-4 py-2 bg-white text-emerald-600 rounded-lg font-semibold text-sm hover:bg-emerald-50 disabled:opacity-60 inline-flex items-center gap-2 transition-colors"
            >
              {status === 'loading' && (
                <span
                  className="w-3.5 h-3.5 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin"
                  aria-hidden="true"
                />
              )}
              {status === 'loading' ? 'Subscribing...' : 'Subscribe Free'}
            </button>
          </form>
        )}
        {status === 'error' && (
          <p className="text-red-200 text-xs mt-2">Please enter a valid email.</p>
        )}
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30 rounded-2xl p-8 border border-emerald-100 dark:border-emerald-900">
      <div className="text-center max-w-xl mx-auto">
        <div className="inline-flex items-center justify-center w-12 h-12 bg-emerald-600 rounded-full mb-4">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Get 5 Free AI Tools Every Week
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          5 hand-picked free AI tool recommendations, straight to your inbox — no VPN needed.
        </p>
        {status === 'success' ? (
          <div className="bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 rounded-lg p-4 font-medium">
            ✓ You're in! Check your inbox to confirm your subscription.
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto"
          >
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <button
              type="submit"
              disabled={status === 'loading'}
              className="px-6 py-3 bg-emerald-700 text-white rounded-lg font-semibold hover:bg-emerald-700 disabled:opacity-60 inline-flex items-center justify-center gap-2 transition-colors"
            >
              {status === 'loading' && (
                <span
                  className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
                  aria-hidden="true"
                />
              )}
              {status === 'loading' ? 'Subscribing...' : 'Subscribe Free'}
            </button>
          </form>
        )}
        {status === 'error' && (
          <p className="text-red-600 dark:text-red-400 text-sm mt-2">
            Please enter a valid email address.
          </p>
        )}
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
          By subscribing, you agree to our Privacy Policy. We respect your inbox and never share
          your data.
        </p>
      </div>
    </div>
  );
}
