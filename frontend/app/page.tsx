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

const exampleQueries = [
  "machine learning for healthcare diagnostics",
  "natural language processing and large language models",
  "computer vision for autonomous vehicles",
  "reinforcement learning and robotics",
  "statistical inference and causal discovery",
  "quantum computing algorithms",
];

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  const [minHIndex, setMinHIndex] = useState(0);
  const [resultCount, setResultCount] = useState(5);
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
          <div className="flex gap-2 mb-4" role="tablist" aria-label="Search method">
            <button
              onClick={() => setSearchMode('text')}
              role="tab"
              aria-selected={searchMode === 'text'}
              aria-controls="text-search-panel"
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
              role="tab"
              aria-selected={searchMode === 'cv'}
              aria-controls="cv-upload-panel"
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
            <div id="cv-upload-panel" role="tabpanel" aria-labelledby="cv-tab">
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
            </div>
          ) : (
            <div id="text-search-panel" role="tabpanel" aria-labelledby="text-tab">
              <h2 className="text-lg font-medium mb-4">
                Describe your research interests
              </h2>
              <Textarea
                aria-label="Describe your research interests"
                placeholder="e.g., statistical learning theory, causal inference, reinforcement learning, convex optimization, Bayesian methods..."
                className="min-h-[120px] mb-4"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
              />

              {!query.trim() && (
                <div className="mt-2 mb-4">
                  <p className="text-xs text-muted-foreground mb-2">Try an example:</p>
                  <div className="flex flex-wrap gap-2">
                    {exampleQueries.map((example) => (
                      <button
                        key={example}
                        onClick={() => setQuery(example)}
                        className="text-xs px-3 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors"
                      >
                        {example}
                      </button>
                    ))}
                  </div>
                </div>
              )}

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
            </div>
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
          <div className="text-center py-12 space-y-4 max-w-2xl mx-auto">
            <Search className="h-12 w-12 mx-auto text-muted-foreground/50" />
            <div>
              <p className="text-muted-foreground font-medium mb-1">
                No faculty found matching your search
              </p>
              {(query || extractedInterests) && (
                <p className="text-sm text-muted-foreground/70 italic">
                  "{(extractedInterests || query).substring(0, 100)}{(extractedInterests || query).length > 100 ? '...' : ''}"
                </p>
              )}
            </div>

            <div className="bg-slate-50 rounded-lg p-4 text-left space-y-3">
              <p className="text-sm font-medium text-slate-700">Suggestions:</p>
              <ul className="text-sm text-slate-600 space-y-2">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5">•</span>
                  <span>Try broader or more general terms (e.g., "machine learning" instead of "few-shot meta-learning for medical imaging")</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5">•</span>
                  <span>Check spelling and try alternative terminology</span>
                </li>
                {minHIndex > 0 && (
                  <li className="flex items-start gap-2">
                    <span className="text-primary mt-0.5">•</span>
                    <span>Lower the minimum h-index filter (currently set to {minHIndex})</span>
                  </li>
                )}
                {universities.length > 0 && (
                  <li className="flex items-start gap-2">
                    <span className="text-primary mt-0.5">•</span>
                    <span>Remove university filters to expand results</span>
                  </li>
                )}
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-0.5">•</span>
                  <span>Try one of the example queries below</span>
                </li>
              </ul>
            </div>

            <div>
              <p className="text-xs text-muted-foreground mb-2">Try these searches:</p>
              <div className="flex flex-wrap gap-2 justify-center">
                {exampleQueries.slice(0, 4).map((example) => (
                  <button
                    key={example}
                    onClick={() => {
                      setQuery(example);
                      setSearchMode('text');
                    }}
                    className="text-xs px-3 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
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
