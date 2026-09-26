"use client";

import { useState } from "react";
import { Upload, CheckCircle2, Loader2 } from "lucide-react";

/**
 * Submit AI Tool page — community flywheel entry point (P2-GROWTH-COMMUNITY-FLYWHEEL-001).
 * Frontend form only. Submission is captured client-side; backend integration
 * (email / database) is handled by window 1. Form validates required fields
 * and shows a success state on submit.
 */
export default function SubmitPage() {
  const [form, setForm] = useState({
    toolName: "",
    toolUrl: "",
    category: "",
    contactEmail: "",
    description: "",
  });
  const [status, setStatus] = useState<"idle" | "submitting" | "success">("idle");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.toolName || !form.toolUrl || !form.contactEmail) return;
    setStatus("submitting");
    // Simulate submission — window 1 will wire real backend
    setTimeout(() => setStatus("success"), 800);
  };

  const update = (key: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [key]: e.target.value }));

  if (status === "success") {
    return (
      <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 pt-24 pb-16 px-4">
        <div className="max-w-xl mx-auto text-center">
          <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900/30">
            <CheckCircle2 className="w-8 h-8 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
          </div>
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-white mb-2">
            Thanks for submitting {form.toolName}!
          </h1>
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">
            Our editorial team will review your tool and evaluate it across our
            6-dimension framework. You will hear back at {form.contactEmail}
            within 7-10 business days.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 pt-24 pb-16 px-4">
      <div className="max-w-xl mx-auto">
        <div className="text-center mb-8">
          <div className="w-14 h-14 mx-auto mb-4 flex items-center justify-center rounded-xl bg-emerald-700 text-white">
            <Upload className="w-6 h-6" aria-hidden="true" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-2 tracking-tight">
            Submit Your AI Tool
          </h1>
          <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
            Get an independent, data-driven review. Top tools get featured in
            our rankings, weekly newsletter, and social shoutouts.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 shadow-sm space-y-5">
          <div>
            <label htmlFor="toolName" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
              Tool Name <span className="text-red-500">*</span>
            </label>
            <input
              id="toolName"
              type="text"
              required
              value={form.toolName}
              onChange={update("toolName")}
              placeholder="e.g. ChatGPT, Midjourney"
              className="w-full px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label htmlFor="toolUrl" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
              Tool Website URL <span className="text-red-500">*</span>
            </label>
            <input
              id="toolUrl"
              type="url"
              required
              value={form.toolUrl}
              onChange={update("toolUrl")}
              placeholder="https://yourtool.com"
              className="w-full px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label htmlFor="category" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
              Category
            </label>
            <select
              id="category"
              value={form.category}
              onChange={update("category")}
              className="w-full px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Select a category</option>
              <option value="chat">AI Chat / Assistant</option>
              <option value="image">AI Image / Art</option>
              <option value="video">AI Video</option>
              <option value="coding">AI Coding</option>
              <option value="writing">AI Writing</option>
              <option value="audio">AI Audio / Music</option>
              <option value="productivity">Productivity</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label htmlFor="contactEmail" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
              Contact Email <span className="text-red-500">*</span>
            </label>
            <input
              id="contactEmail"
              type="email"
              required
              value={form.contactEmail}
              onChange={update("contactEmail")}
              placeholder="you@company.com"
              className="w-full px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
              What makes this tool special?
            </label>
            <textarea
              id="description"
              rows={3}
              value={form.description}
              onChange={update("description")}
              placeholder="Brief description, key features, target users..."
              className="w-full px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 resize-none"
            />
          </div>

          <button
            type="submit"
            disabled={status === "submitting"}
            className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 bg-emerald-700 hover:bg-emerald-600 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md active:scale-[0.98] disabled:opacity-60"
          >
            {status === "submitting" ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                Submitting...
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" aria-hidden="true" />
                Submit for Review
              </>
            )}
          </button>

          <p className="text-xs text-zinc-500 dark:text-zinc-400 text-center">
            Free for creators. We do not accept paid placements. All reviews
            follow our public 6-dimension methodology.
          </p>
        </form>
      </div>
    </main>
  );
}
