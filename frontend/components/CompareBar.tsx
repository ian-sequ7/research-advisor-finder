"use client";

import { SearchResult } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { X, GitCompare } from "lucide-react";
import { cn } from "@/lib/utils";

interface CompareBarProps {
  selected: SearchResult[];
  onRemove: (id: number) => void;
  onCompare: () => void;
  onClear: () => void;
}

export function CompareBar({
  selected,
  onRemove,
  onCompare,
  onClear,
}: CompareBarProps) {
  if (selected.length === 0) return null;

  const canCompare = selected.length >= 2;

  return (
    <div
      className={cn(
        "fixed bottom-0 left-0 right-0 z-50 border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80",
        "transition-transform duration-300 ease-in-out",
        "animate-in slide-in-from-bottom"
      )}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between gap-4">
          {/* Selected faculty chips */}
          <div className="flex flex-1 items-center gap-2 overflow-x-auto">
            <span className="shrink-0 text-sm font-medium text-muted-foreground">
              Selected ({selected.length}):
            </span>
            <div className="flex gap-2 overflow-x-auto pb-1">
              {selected.map((result) => (
                <Badge
                  key={result.faculty.id}
                  variant="secondary"
                  className="shrink-0 gap-1.5 pl-3 pr-2"
                >
                  <span className="max-w-[200px] truncate">
                    {result.faculty.name}
                  </span>
                  <button
                    onClick={() => onRemove(result.faculty.id)}
                    className="rounded-full hover:bg-secondary-foreground/20 p-0.5 transition-colors"
                    aria-label={`Remove ${result.faculty.name}`}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex shrink-0 items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onClear}
              aria-label="Clear all selections"
            >
              Clear
            </Button>
            <Button
              size="sm"
              onClick={onCompare}
              disabled={!canCompare}
              className="gap-1.5"
              aria-label={`Compare ${selected.length} faculty members`}
            >
              <GitCompare className="h-4 w-4" />
              Compare ({selected.length})
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
