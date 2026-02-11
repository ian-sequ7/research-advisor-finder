'use client';

import { ChatExplorer } from '@/components/ChatExplorer';
import { Header } from '@/components/Header';

export default function ExplorePage() {
  return (
    <main className="min-h-screen bg-slate-50">
      <Header currentPage="explore" />

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold mb-1">
            Explore Research Directions
          </h1>
          <p className="text-sm text-muted-foreground">
            Browse papers interactively to narrow from a broad interest to a
            specific direction, then find matched faculty.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border p-6">
          <ChatExplorer />
        </div>
      </div>
    </main>
  );
}
