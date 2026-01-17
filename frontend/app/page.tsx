'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { SearchResult, searchFaculty, uploadCV } from '@/lib/api';
import CVUpload from '@/components/CVUpload';
import { ResultCard } from '@/components/ResultCard';
import { ResultSkeleton } from '@/components/ResultSkeleton';
import { Filters } from '@/components/Filters';
import { Loader2, Search, AlertCircle } from 'lucide-react';
import { CompareBar } from '@/components/CompareBar';
import { CompareModal } from '@/components/CompareModal';
import { Header } from '@/components/Header';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  const [minHIndex, setMinHIndex] = useState(0);
  const [resultCount, setResultCount] = useState(10);
  const [universities, setUniversities] = useState<string[]>([]);

  const [searchMode, setSearchMode] = useState<'text' | 'cv'>('text');
  const [extractedInterests, setExtractedInterests] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const [compareList, setCompareList] = useState<SearchResult[]>([]);
  const [showCompare, setShowCompare] = useState(false);

  const toggleCompare = (result: SearchResult) => {
    setCompareList((prev) => {
      const exists = prev.some((r) => r.faculty.id === result.faculty.id);
      if (exists) {
        return prev.filter((r) => r.faculty.id !== result.faculty.id);
      }
      if (prev.length >= 3) {
        return prev;
      }
      return [...prev, result];
    });
  };

  const clearCompare = () => {
    setCompareList([]);
  };

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setSearched(true);

    try {
      const data = await searchFaculty(query, resultCount, minHIndex, universities);
      setResults(data);
    } catch (err) {
      setError('Search failed. Please check your connection and try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.metaKey) {
      handleSearch();
    }
  };

  const handleCVUpload = async (file: File) => {
    setLoading(true);
    setUploadError(null);
    setExtractedInterests(null);
    setError(null);
    setSearched(true);

    try {
      const response = await uploadCV({
        file,
        limit: resultCount,
        minHIndex: minHIndex,
        universities: universities.length > 0 ? universities : undefined,
      });

      setExtractedInterests(response.extracted_interests);
      setResults(response.results);
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <Header currentPage="search" />

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <div className="flex gap-2 mb-4">
            <button
              onClick={() => setSearchMode('text')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                searchMode === 'text'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              Text Search
            </button>
            <button
              onClick={() => setSearchMode('cv')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                searchMode === 'cv'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              Upload CV
            </button>
          </div>

          {searchMode === 'cv' ? (
            <>
              <h2 className="text-lg font-medium mb-4">
                Upload your CV/Resume
              </h2>
              <div className="mb-4">
                <CVUpload
                  onUpload={handleCVUpload}
                  isLoading={loading}
                  error={uploadError}
                />
              </div>
              {extractedInterests && (
                <div className="mt-4 p-4 bg-slate-50 rounded-lg border">
                  <h3 className="font-medium text-slate-700 mb-2">Extracted Research Interests:</h3>
                  <p className="text-sm text-slate-600 whitespace-pre-wrap">{extractedInterests}</p>
                </div>
              )}
              <div className="mt-4">
                <Filters
                  minHIndex={minHIndex}
                  setMinHIndex={setMinHIndex}
                  resultCount={resultCount}
                  setResultCount={setResultCount}
                  universities={universities}
                  setUniversities={setUniversities}
                />
              </div>
            </>
          ) : (
            <>
              <h2 className="text-lg font-medium mb-4">
                Describe your research interests
              </h2>
              <Textarea
                placeholder="e.g., statistical learning theory, causal inference, reinforcement learning, convex optimization, Bayesian methods..."
                className="min-h-[120px] mb-4"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
              />

              <div className="mb-4">
                <Filters
                  minHIndex={minHIndex}
                  setMinHIndex={setMinHIndex}
                  resultCount={resultCount}
                  setResultCount={setResultCount}
                  universities={universities}
                  setUniversities={setUniversities}
                />
              </div>

              <div className="flex items-center justify-between">
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
                <span className="text-xs text-muted-foreground hidden sm:block">
                  ⌘ + Enter to search
                </span>
              </div>
            </>
          )}
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-center gap-2">
            <AlertCircle className="h-5 w-5" />
            {error}
          </div>
        )}

        {loading && (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <ResultSkeleton key={i} />
            ))}
          </div>
        )}

        {!loading && results.length > 0 && (
          <div>
            <h2 className="text-lg font-medium mb-4">
              Top {results.length} Matches
            </h2>
            <div className="space-y-4 pb-20">
              {results.map((result, index) => (
                <ResultCard
                  key={result.faculty.id}
                  result={result}
                  rank={index + 1}
                  interests={extractedInterests || query}
                  onCompareToggle={toggleCompare}
                  isInCompare={compareList.some((r) => r.faculty.id === result.faculty.id)}
                  compareDisabled={compareList.length >= 3 && !compareList.some((r) => r.faculty.id === result.faculty.id)}
                />
              ))}
            </div>
          </div>
        )}

        {!loading && searched && results.length === 0 && !error && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">
              No faculty found matching your criteria. Try adjusting your filters or search terms.
            </p>
          </div>
        )}
      </div>

      <CompareBar
        selected={compareList}
        onRemove={(id) => setCompareList((prev) => prev.filter((r) => r.faculty.id !== id))}
        onCompare={() => setShowCompare(true)}
        onClear={clearCompare}
      />

      <CompareModal
        isOpen={showCompare}
        onClose={() => setShowCompare(false)}
        selected={compareList}
        interests={extractedInterests || query}
      />
    </main>
  );
}
