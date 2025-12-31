'use client';

import { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { SearchResult, getExplanation } from '@/lib/api';
import { ExternalLink, Loader2, Sparkles, FileText } from 'lucide-react';

interface ResultCardProps {
	result: SearchResult;
	rank: number;
	interests: string;
}

export function ResultCard({ result, rank, interests }: ResultCardProps) {
  const [explanation, setExplanation] = useState<string | null>(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);

  const { faculty, similarity, papers } = result;

  const handleExplain = async () => {
    setLoadingExplanation(true);
    try {
      const text = await getExplanation(interests, faculty.id);
      setExplanation(text);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingExplanation(false);
    }
  };

  const matchColor = similarity > 0.5
    ? 'bg-green-100 text-green-800'
    : similarity > 0.35
    ? 'bg-yellow-100 text-yellow-800'
    : 'bg-slate-100 text-slate-800';

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm text-muted-foreground">#{rank}</span>
              <h3 className="text-lg font-semibold">{faculty.name}</h3>
            </div>
            <p className="text-sm text-muted-foreground">{faculty.affiliation}</p>
          </div>
          <Badge className={matchColor}>
            {Math.round(similarity * 100)}% match
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Stats */}
        <div className="flex gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">H-Index: </span>
            <span className="font-medium">{faculty.h_index ?? 'N/A'}</span>
          </div>
          <div>
            <span className="text-muted-foreground">Papers: </span>
            <span className="font-medium">{faculty.paper_count ?? 'N/A'}</span>
          </div>
          {faculty.semantic_scholar_id && (
            
              href={`https://semanticscholar.org/author/${faculty.semantic_scholar_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline flex items-center gap-1"
            >
              Semantic Scholar <ExternalLink className="h-3 w-3" />
            </a>
          )}
        </div>

        <Separator />

		{/* Papers */}
        {papers.length > 0 && (
          <div>
            <h4 className="text-sm font-medium mb-2 flex items-center gap-1">
              <FileText className="h-4 w-4" /> Top Papers
            </h4>
            <ul className="space-y-1">
              {papers.slice(0, 3).map((paper) => (
                <li key={paper.id} className="text-sm text-muted-foreground">
                  • {paper.title} ({paper.year})
                </li>
              ))}
            </ul>
          </div>
        )}

		{/* Explanation */}
        {explanation ? (
          <div className="bg-primary/5 rounded-lg p-4">
            <h4 className="text-sm font-medium mb-2 flex items-center gap-1">
              <Sparkles className="h-4 w-4" /> Why this matches
            </h4>
            <p className="text-sm">{explanation}</p>
          </div>
        ) : (
          <Button
            variant="outline"
            size="sm"
            onClick={handleExplain}
            disabled={loadingExplanation}
          >
            {loadingExplanation ? (
              <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generating...</>
            ) : (
              <><Sparkles className="mr-2 h-4 w-4" /> Explain Match</>
            )}
          </Button>
        )}
      </CardContent>
    </Card>
  );
}


