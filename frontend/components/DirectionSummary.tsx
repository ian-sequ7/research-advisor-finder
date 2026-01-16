'use client';

import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ExploreFinishResponse } from '@/lib/api';
import { Target, User, FileText, ExternalLink, Sparkles } from 'lucide-react';

interface DirectionSummaryProps {
  result: ExploreFinishResponse;
}

export function DirectionSummary({ result }: DirectionSummaryProps) {
  return (
    <div className="space-y-6">
      <Card className="border-primary/20 bg-primary/5">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Target className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold">Your Research Direction</h2>
          </div>
        </CardHeader>
        <CardContent>
          <h3 className="text-xl font-bold mb-2">{result.direction_summary}</h3>
          <p className="text-muted-foreground">{result.direction_description}</p>
        </CardContent>
      </Card>

      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <User className="h-5 w-5" />
          Matched Faculty ({result.faculty_matches.length})
        </h3>
        <div className="space-y-4">
          {result.faculty_matches.map((match, index) => (
            <Card key={match.faculty.id}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm text-muted-foreground">#{index + 1}</span>
                      <h4 className="text-lg font-semibold">{match.faculty.name}</h4>
                    </div>
                    <p className="text-sm text-muted-foreground">{match.faculty.affiliation}</p>
                    {match.faculty.research_tags && match.faculty.research_tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {match.faculty.research_tags.slice(0, 3).map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    )}
                  </div>
                  <Badge className="bg-green-100 text-green-800">
                    {Math.round(match.similarity * 100)}% match
                  </Badge>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="flex gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">H-Index: </span>
                    <span className="font-medium">{match.faculty.h_index ?? 'N/A'}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Papers: </span>
                    <span className="font-medium">{match.faculty.paper_count ?? 'N/A'}</span>
                  </div>
                  {match.faculty.semantic_scholar_id && (
                    <a
                      href={`https://semanticscholar.org/author/${match.faculty.semantic_scholar_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline flex items-center gap-1"
                    >
                      Profile <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>

                <Separator />

                <div className="bg-primary/5 rounded-lg p-3">
                  <div className="flex items-center gap-1 text-sm font-medium mb-1">
                    <Sparkles className="h-4 w-4" />
                    Why this matches
                  </div>
                  <p className="text-sm text-muted-foreground">{match.explanation}</p>
                </div>

                {match.key_paper && (
                  <div className="text-sm">
                    <div className="flex items-center gap-1 text-muted-foreground mb-1">
                      <FileText className="h-4 w-4" />
                      Key Paper
                    </div>
                    <p className="italic">{match.key_paper}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
