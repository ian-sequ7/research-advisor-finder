'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { ResearchTags } from '@/components/ResearchTags';
import { SearchResult } from '@/lib/api';
import { ExternalLink, FileText } from 'lucide-react';

interface CompareModalProps {
  isOpen: boolean;
  onClose: () => void;
  selected: SearchResult[];
  interests: string;
}

export function CompareModal({ isOpen, onClose, selected, interests }: CompareModalProps) {
  const getMatchColor = (similarity: number) => {
    if (similarity > 0.5) return 'bg-green-100 text-green-800';
    if (similarity > 0.35) return 'bg-yellow-100 text-yellow-800';
    return 'bg-slate-100 text-slate-800';
  };

  const getFacultyBadge = (hIndex: number | null) => {
    if (hIndex === null || hIndex === undefined) return null;
    if (hIndex < 30) {
      return { label: 'Junior Faculty', className: 'bg-orange-100 text-orange-800' };
    }
    if (hIndex > 30 && hIndex < 60) {
      return { label: 'Rising Junior Faculty', className: 'bg-yellow-100 text-yellow-800' };
    }
    if (hIndex > 60) {
      return { label: 'Established Faculty', className: 'bg-green-100 text-green-800' };
    }
    return null;
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Compare Faculty ({selected.length})</DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {selected.map((result) => {
            const { faculty, similarity, papers } = result;
            const matchColor = getMatchColor(similarity);
            const facultyBadge = getFacultyBadge(faculty.h_index);

            return (
              <div
                key={faculty.id}
                className="border rounded-lg p-4 bg-card space-y-4"
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="text-lg font-semibold leading-tight">{faculty.name}</h3>
                    <Badge className={matchColor}>
                      {Math.round(similarity * 100)}%
                    </Badge>
                  </div>

                  {facultyBadge && (
                    <Badge className={facultyBadge.className}>
                      {facultyBadge.label}
                    </Badge>
                  )}

                  <p className="text-sm text-muted-foreground">{faculty.affiliation}</p>
                  <ResearchTags tags={faculty.research_tags} maxDisplay={3} />
                </div>

                <div className="flex gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">H-Index: </span>
                    <span className="font-medium">{faculty.h_index ?? 'N/A'}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Papers: </span>
                    <span className="font-medium">{faculty.paper_count ?? 'N/A'}</span>
                  </div>
                </div>

                {faculty.semantic_scholar_id && (
                  <a
                    href={`https://semanticscholar.org/author/${faculty.semantic_scholar_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline flex items-center gap-1 text-sm"
                  >
                    Semantic Scholar <ExternalLink className="h-3 w-3" />
                  </a>
                )}

                {papers.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium mb-2 flex items-center gap-1">
                      <FileText className="h-4 w-4" /> Top Papers
                    </h4>
                    <ul className="space-y-1.5">
                      {papers.slice(0, 3).map((paper) => (
                        <li key={paper.id} className="text-sm text-muted-foreground flex items-start gap-1">
                          <span className="mt-0.5">•</span>
                          <span className="flex-1">
                            {paper.title.length > 60 ? `${paper.title.slice(0, 60)}...` : paper.title}
                            {paper.year && ` (${paper.year})`}
                            {paper.citation_count !== null && paper.citation_count > 0 && (
                              <Badge variant="outline" className="ml-1 text-xs py-0 h-5">
                                {paper.citation_count} cites
                              </Badge>
                            )}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </DialogContent>
    </Dialog>
  );
}
