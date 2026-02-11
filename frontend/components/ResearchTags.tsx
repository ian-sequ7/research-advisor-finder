'use client';

import { Badge } from '@/components/ui/badge';

interface ResearchTagsProps {
  tags: string[];
  maxDisplay?: number;
}

export function ResearchTags({ tags, maxDisplay = 5 }: ResearchTagsProps) {
  if (!tags || tags.length === 0) {
    return null;
  }

  const displayTags = tags.slice(0, maxDisplay);
  const remainingCount = tags.length - maxDisplay;

  return (
    <div className="flex flex-wrap gap-1.5 mt-2">
      {displayTags.map((tag) => (
        <Badge
          key={tag}
          variant="secondary"
          className="text-xs font-normal"
        >
          {tag}
        </Badge>
      ))}
      {remainingCount > 0 && (
        <Badge
          variant="secondary"
          className="text-xs font-normal bg-slate-100 text-slate-600"
        >
          +{remainingCount} more
        </Badge>
      )}
    </div>
  );
}
