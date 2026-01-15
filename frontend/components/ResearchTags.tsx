'use client';

import { Badge } from '@/components/ui/badge';

interface ResearchTagsProps {
  tags: string[];
  maxDisplay?: number;
}

/**
 * Renders research area tags as colored badges.
 * Truncates with "+N more" if > maxDisplay.
 * Graceful empty state (renders nothing, not "No tags").
 */
export function ResearchTags({ tags, maxDisplay = 5 }: ResearchTagsProps) {
  // Return nothing for empty tags (graceful empty state)
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
          className="text-xs font-normal bg-blue-50 text-blue-700 hover:bg-blue-100"
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
