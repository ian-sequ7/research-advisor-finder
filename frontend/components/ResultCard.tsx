'use client';

import { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { SearchResult, getExplanation, ExplanationBreakdown } from '@/lib/api';
import { ResearchTags } from '@/components/ResearchTags';
import { ExternalLink, Loader2, Sparkles, FileText, Plus, Check } from 'lucide-react';

interface ResultCardProps {
  result: SearchResult;
  rank: number;
  interests: string;
  onCompareToggle?: (result: SearchResult) => void;
  isInCompare?: boolean;
  compareDisabled?: boolean;
}

export function ResultCard({ result, rank, interests, onCompareToggle, isInCompare, compareDisabled }: ResultCardProps) {
  const [explanation, setExplanation] = useState<string | null>(null);
  const [breakdown, setBreakdown] = useState<ExplanationBreakdown | null>(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);

  const { faculty, similarity, papers } = result;

  const handleExplain = async () => {
    setLoadingExplanation(true);
    try {
      const response = await getExplanation(interests, faculty.id);
      setExplanation(response.explanation);
      setBreakdown(response.breakdown || null);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingExplanation(false);
    }
  };

  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-slate-100 text-slate-600';
      default:
        return 'bg-slate-100 text-slate-600';
    }
  };

  const getLevelIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return '✓';
      case 'medium':
        return '~';
      case 'low':
        return '○';
      default:
        return '○';
    }
  };

  const matchColor = similarity > 0.5
    ? 'bg-green-100 text-green-800'
    : similarity > 0.35
    ? 'bg-yellow-100 text-yellow-800'
    : 'bg-slate-100 text-slate-800';

  const getFacultyBadge = () => {                                                                                                                                                                                     
    if (faculty.h_index === null || faculty.h_index === undefined) return null;                                                                                                                                       
    if (faculty.h_index < 30) {                                                                                                                                                                                       
      return { label: 'Junior Faculty', className: 'bg-orange-100 text-orange-800' };
    }
    if(faculty.h_index > 30 && faculty.h_index < 60) {
      return{ label: 'Rising Junior Faculty', className: 'bg-yellow-100 text-yellow-800'}
    } 
    if (faculty.h_index > 60) {
      return { label: 'Established Faculty', className: 'bg-green-100 text-green-800' };
    }
    return null; 
  };

  const facultyBadge = getFacultyBadge();

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm text-muted-foreground">#{rank}</span>
               <h3 className="text-lg font-semibold">{faculty.name}</h3>
                {facultyBadge && (
                  <Badge className={facultyBadge.className}>
                    {facultyBadge.label}
                  </Badge>
                )}
            </div>
            <p className="text-sm text-muted-foreground">{faculty.affiliation}</p>
            <ResearchTags tags={faculty.research_tags} />
          </div>
          <Badge className={matchColor}>
            {Math.round(similarity * 100)}% match
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
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
            <a
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

        {papers.length > 0 && (
          <div>
            <h4 className="text-sm font-medium mb-2 flex items-center gap-1">
              <FileText className="h-4 w-4" /> Top Papers
            </h4>
            <ul className="space-y-1.5">
              {papers.slice(0, 5).map((paper) => (
                <li key={paper.id} className="text-sm text-muted-foreground flex items-start gap-1">
                  <span className="mt-0.5">•</span>
                  <span className="flex-1">
                    {paper.title.length > 80 ? `${paper.title.slice(0, 80)}...` : paper.title}
                    {paper.year && ` (${paper.year})`}
                    {paper.citation_count !== null && paper.citation_count > 0 && (
                      <Badge variant="outline" className="ml-2 text-xs py-0 h-5">
                        {paper.citation_count} citations
                      </Badge>
                    )}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {explanation ? (
          <div className="bg-primary/5 rounded-lg p-4 space-y-3">
            <h4 className="text-sm font-medium mb-2 flex items-center gap-1">
              <Sparkles className="h-4 w-4" /> Why this matches
            </h4>
            <p className="text-sm">{explanation}</p>

            {breakdown && (
              <div className="flex flex-wrap gap-2 pt-2 border-t border-primary/10">
                {breakdown.topic_alignment && (
                  <Badge className={`${getLevelColor(breakdown.topic_alignment.level)} text-xs`}>
                    {getLevelIcon(breakdown.topic_alignment.level)} Topic: {breakdown.topic_alignment.level}
                  </Badge>
                )}
                {breakdown.paper_relevance && (
                  <Badge className={`${getLevelColor(breakdown.paper_relevance.level)} text-xs`}>
                    {getLevelIcon(breakdown.paper_relevance.level)} Papers: {breakdown.paper_relevance.level}
                  </Badge>
                )}
                {breakdown.research_fit && (
                  <Badge className={`${getLevelColor(breakdown.research_fit.level)} text-xs`}>
                    {getLevelIcon(breakdown.research_fit.level)} Fit: {breakdown.research_fit.level}
                  </Badge>
                )}
              </div>
            )}
          </div>
        ) : null}

        <div className="flex gap-2">
          {!explanation && (
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
          {onCompareToggle && (
            <Button
              variant={isInCompare ? "default" : "outline"}
              size="sm"
              onClick={() => onCompareToggle(result)}
              disabled={compareDisabled && !isInCompare}
              title={compareDisabled && !isInCompare ? "Maximum 3 faculty can be compared" : undefined}
              className={isInCompare ? "bg-blue-600 hover:bg-blue-700" : ""}
            >
              {isInCompare ? (
                <><Check className="mr-2 h-4 w-4" /> In Compare</>
              ) : (
                <><Plus className="mr-2 h-4 w-4" /> Add to Compare</>
              )}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
