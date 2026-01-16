'use client';

import { ChatExplorer } from '@/components/ChatExplorer';
import { Header } from '@/components/Header';
import { Compass } from 'lucide-react';

export default function ExplorePage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <Header currentPage="explore" />

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm mb-4">
            <Compass className="h-4 w-4" />
            Research Path Explorer
          </div>
          <h1 className="text-3xl font-bold mb-2">
            Discover Your Research Direction
          </h1>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Not sure what you want to research? Explore papers interactively and
            we&apos;ll help you narrow down from a broad interest to a specific
            direction with matched faculty.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border p-6">
          <ChatExplorer />
        </div>
      </div>
    </main>
  );
}
