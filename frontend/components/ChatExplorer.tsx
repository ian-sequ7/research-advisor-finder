'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { PaperCard } from '@/components/PaperCard';
import { DirectionSummary } from '@/components/DirectionSummary';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  ExplorePaper,
  ExploreFinishResponse,
  startExploration,
  respondToExploration,
  finishExploration,
} from '@/lib/api';
import { Loader2, Send, RotateCcw, Users, ArrowRight, FileQuestion } from 'lucide-react';

type ExploreState = 'start' | 'exploring' | 'ready' | 'finished';

function PaperCardSkeleton() {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2">
              <Skeleton className="h-5 w-8" />
              <Skeleton className="h-4 w-3/4" />
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <Skeleton className="h-3 w-24" />
              <Skeleton className="h-3 w-16" />
              <Skeleton className="h-3 w-20" />
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="space-y-2">
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-5/6" />
          <Skeleton className="h-3 w-4/5" />
        </div>
      </CardContent>
    </Card>
  );
}

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
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [state]);

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
    setShowResetConfirm(false);
  };

  const handleResetClick = () => {
    if (state === 'start') {
      handleReset();
    } else {
      setShowResetConfirm(true);
    }
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

  if (state === 'finished' && result) {
    return (
      <div className="space-y-6">
        {result.faculty_matches.length === 0 ? (
          <div className="space-y-6">
            <Card className="border-primary/20 bg-primary/5">
              <CardHeader>
                <h2 className="text-lg font-semibold">Your Research Direction</h2>
              </CardHeader>
              <CardContent>
                <h3 className="text-xl font-bold mb-2">{result.direction_summary}</h3>
                <p className="text-muted-foreground">{result.direction_description}</p>
              </CardContent>
            </Card>

            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Users className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">
                No faculty matches found for this direction.
              </p>
            </div>
          </div>
        ) : (
          <DirectionSummary result={result} />
        )}

        <div className="flex justify-center">
          <Button variant="outline" onClick={handleResetClick}>
            <RotateCcw className="mr-2 h-4 w-4" /> Start New Exploration
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>Round {round}</span>
        {state === 'ready' && (
          <span className="text-green-600 font-medium">Ready to see faculty matches!</span>
        )}
      </div>

      <div className="bg-slate-50 rounded-lg p-4 border">
        <p className="text-sm">{prompt}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {loading ? (
          <>
            <PaperCardSkeleton />
            <PaperCardSkeleton />
            <PaperCardSkeleton />
            <PaperCardSkeleton />
          </>
        ) : papers.length === 0 ? (
          <div className="col-span-2 flex flex-col items-center justify-center py-12 text-center">
            <FileQuestion className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              No papers found. Try describing your interests differently.
            </p>
          </div>
        ) : (
          papers.map((paper, index) => (
            <PaperCard key={paper.id} paper={paper} index={index} />
          ))
        )}
      </div>

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

          <Button variant="ghost" onClick={handleResetClick}>
            <RotateCcw className="mr-2 h-4 w-4" /> Start Over
          </Button>
        </div>

        <p className="text-xs text-muted-foreground">
          Tip: Press Cmd+Enter to submit
        </p>
      </div>

      <Dialog open={showResetConfirm} onOpenChange={setShowResetConfirm}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Start Over?</DialogTitle>
            <DialogDescription>
              This will discard your exploration progress. You&apos;ll need to start from the beginning.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowResetConfirm(false)}>
              Cancel
            </Button>
            <Button onClick={handleReset}>
              Start Over
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
