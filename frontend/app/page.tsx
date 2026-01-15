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
import { Loader2, Search, GraduationCap, AlertCircle, BookOpen } from 'lucide-react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  const [minHIndex, setMinHIndex] = useState(0);
  const [resultCount, setResultCount] = useState(10);
  const [universities, setUniversities] = useState<string[]>([]);

  // CV Upload state
  const [searchMode, setSearchMode] = useState<'text' | 'cv'>('text');
  const [extractedInterests, setExtractedInterests] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

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
      {/* Header */}
      <div className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <GraduationCap className="h-6 w-6 text-primary" />
            <h1 className="text-xl font-semibold">Research Advisor Finder</h1>
          </div>
          <Link
            href="/resources"
            className="text-sm text-muted-foreground hover:text-primary flex items-center gap-1"
          >
            <BookOpen className="h-4 w-4" />
            Resources
          </Link>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          {/* Mode Toggle */}
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
              {/* Filters */}
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
                placeholder="I'm interested in mechanistic interpretability, neural network pruning, and understanding how large language models represent knowledge internally..."
                className="min-h-[120px] mb-4"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
              />

              {/* Filters */}
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

        {/* Error */}
        {error && (
          <div className="bg-red-50 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-center gap-2">
            <AlertCircle className="h-5 w-5" />
            {error}
          </div>
        )}

        {/* Loading Skeletons */}
        {loading && (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <ResultSkeleton key={i} />
            ))}
          </div>
        )}

        {/* Results */}
        {!loading && results.length > 0 && (
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
                  interests={extractedInterests || query}
                />
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && searched && results.length === 0 && !error && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">
              No faculty found matching your criteria. Try adjusting your filters or search terms.
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
