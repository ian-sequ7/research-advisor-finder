'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { PaperCard } from '@/components/PaperCard';
import { DirectionSummary } from '@/components/DirectionSummary';
import {
  ExplorePaper,
  ExploreFinishResponse,
  startExploration,
  respondToExploration,
  finishExploration,
} from '@/lib/api';
import { Loader2, Send, RotateCcw, Users, ArrowRight } from 'lucide-react';

type ExploreState = 'start' | 'exploring' | 'ready' | 'finished';

export function ChatExplorer() {
  const [state, setState] = useState<ExploreState>('start');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [initialInterest, setInitialInterest] = useState('');
  const [papers, setPapers] = useState<ExplorePaper[]>([]);
  const [prompt, setPrompt] = useState('');
  const [userResponse, setUserResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ExploreFinishResponse | null>(null);
  const [round, setRound] = useState(0);

  const handleStart = async () => {
    if (!initialInterest.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await startExploration(initialInterest);
      setSessionId(response.session_id);
      setPapers(response.papers);
      setPrompt(response.prompt);
      setState('exploring');
      setRound(1);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start exploration');
    } finally {
      setLoading(false);
    }
  };

  const handleRespond = async () => {
    if (!sessionId || !userResponse.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await respondToExploration(sessionId, userResponse);
      setPapers(response.papers);
      setPrompt(response.prompt);
      setUserResponse('');
      setRound((r) => r + 1);

      if (response.is_ready) {
        setState('ready');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process response');
    } finally {
      setLoading(false);
    }
  };

  const handleFinish = async () => {
    if (!sessionId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await finishExploration(sessionId);
      setResult(response);
      setState('finished');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to finish exploration');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setState('start');
    setSessionId(null);
    setInitialInterest('');
    setPapers([]);
    setPrompt('');
    setUserResponse('');
    setResult(null);
    setRound(0);
    setError(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.metaKey) {
      if (state === 'start') {
        handleStart();
      } else if (state === 'exploring' || state === 'ready') {
        handleRespond();
      }
    }
  };

  // Start state - enter initial interest
  if (state === 'start') {
    return (
      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-medium mb-2">What are you interested in?</h2>
          <p className="text-sm text-muted-foreground mb-4">
            Enter a broad research area and we&apos;ll help you narrow it down through paper exploration.
          </p>
        </div>

        <Input
          placeholder="e.g., machine learning, natural language processing, computer vision..."
          value={initialInterest}
          onChange={(e) => setInitialInterest(e.target.value)}
          onKeyDown={handleKeyDown}
          className="text-lg"
        />

        {error && (
          <p className="text-sm text-red-600">{error}</p>
        )}

        <Button
          onClick={handleStart}
          disabled={loading || !initialInterest.trim()}
          className="w-full sm:w-auto"
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Starting...
            </>
          ) : (
            <>
              Start Exploring <ArrowRight className="ml-2 h-4 w-4" />
            </>
          )}
        </Button>
      </div>
    );
  }

  // Finished state - show results
  if (state === 'finished' && result) {
    return (
      <div className="space-y-6">
        <DirectionSummary result={result} />

        <div className="flex justify-center">
          <Button variant="outline" onClick={handleReset}>
            <RotateCcw className="mr-2 h-4 w-4" /> Start New Exploration
          </Button>
        </div>
      </div>
    );
  }

  // Exploring or Ready state
  return (
    <div className="space-y-6">
      {/* Progress indicator */}
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>Round {round}</span>
        {state === 'ready' && (
          <span className="text-green-600 font-medium">Ready to see faculty matches!</span>
        )}
      </div>

      {/* Prompt */}
      <div className="bg-slate-50 rounded-lg p-4 border">
        <p className="text-sm">{prompt}</p>
      </div>

      {/* Papers grid */}
      <div className="grid gap-4 md:grid-cols-2">
        {papers.map((paper, index) => (
          <PaperCard key={paper.id} paper={paper} index={index} />
        ))}
      </div>

      {/* User response input */}
      <div className="space-y-3">
        <Textarea
          placeholder="Share your thoughts... Which papers interest you? What aspects draw you in? What's missing?"
          value={userResponse}
          onChange={(e) => setUserResponse(e.target.value)}
          onKeyDown={handleKeyDown}
          className="min-h-[100px]"
        />

        {error && (
          <p className="text-sm text-red-600">{error}</p>
        )}

        <div className="flex flex-wrap gap-2">
          <Button
            onClick={handleRespond}
            disabled={loading || !userResponse.trim()}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Processing...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" /> Continue Exploring
              </>
            )}
          </Button>

          {state === 'ready' && (
            <Button
              variant="default"
              className="bg-green-600 hover:bg-green-700"
              onClick={handleFinish}
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Finding faculty...
                </>
              ) : (
                <>
                  <Users className="mr-2 h-4 w-4" /> Show Me Faculty
                </>
              )}
            </Button>
          )}

          <Button variant="ghost" onClick={handleReset}>
            <RotateCcw className="mr-2 h-4 w-4" /> Start Over
          </Button>
        </div>

        <p className="text-xs text-muted-foreground">
          Tip: Press Cmd+Enter to submit
        </p>
      </div>
    </div>
  );
}
