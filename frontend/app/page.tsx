'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { SearchResult, searchFaculty } from '@/lib/api';
import { ResultCard } from '@/components/ResultCard';
import { Loader2, Search, GraduationCap } from 'lucide-react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await searchFaculty(query);
      setResults(data);
    } catch (err) {
      setError('Search failed. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
      <div className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-2">
          <GraduationCap className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-semibold">Research Advisor Finder</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h2 className="text-lg font-medium mb-4">
            Describe your research interests
          </h2>
          <Textarea
            placeholder="I'm interested in mechanistic interpretability..."
            className="min-h-[120px] mb-4"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="w-full sm:w-auto"
          >
            {loading ? (
              <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Searching...</>
            ) : (
              <><Search className="mr-2 h-4 w-4" /> Find Advisors</>
            )}
          </Button>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Results */}
        {results.length > 0 && (
          <div>
            <h2 className="text-lg font-medium mb-4">
              Top {results.length} Matches
            </h2>
            <div className="space-y-4">
              {results.map((result, index) => (
                <ResultCard
                  key={result.faculty.id}
                  result={result}
                  rank={index + 1}
                  interests={query}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
