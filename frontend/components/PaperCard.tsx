'use client';

import { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExplorePaper } from '@/lib/api';
import { ChevronDown, ChevronUp, User, Calendar, BookOpen } from 'lucide-react';

interface PaperCardProps {
  paper: ExplorePaper;
  index: number;
}

export function PaperCard({ paper, index }: PaperCardProps) {
  const [expanded, setExpanded] = useState(false);

  const truncatedAbstract = paper.abstract && paper.abstract.length > 200
    ? paper.abstract.slice(0, 200) + '...'
    : paper.abstract;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="outline" className="text-xs">
                {index + 1}
              </Badge>
              <h3 className="font-medium text-sm leading-tight">
                {paper.title}
              </h3>
            </div>
            <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground mt-2">
              {paper.faculty_name && (
                <span className="flex items-center gap-1">
                  <User className="h-3 w-3" />
                  {paper.faculty_name}
                </span>
              )}
              {paper.year && (
                <span className="flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {paper.year}
                </span>
              )}
              {paper.venue && (
                <span className="flex items-center gap-1">
                  <BookOpen className="h-3 w-3" />
                  {paper.venue.length > 30 ? paper.venue.slice(0, 30) + '...' : paper.venue}
                </span>
              )}
            </div>
          </div>
        </div>
      </CardHeader>

      {paper.abstract && (
        <CardContent className="pt-0">
          <p className="text-sm text-muted-foreground leading-relaxed">
            {expanded ? paper.abstract : truncatedAbstract}
          </p>
          {paper.abstract.length > 200 && (
            <Button
              variant="ghost"
              size="sm"
              className="mt-2 h-6 px-2 text-xs"
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? (
                <>
                  <ChevronUp className="h-3 w-3 mr-1" /> Show less
                </>
              ) : (
                <>
                  <ChevronDown className="h-3 w-3 mr-1" /> Read more
                </>
              )}
            </Button>
          )}
        </CardContent>
      )}
    </Card>
  );
}
