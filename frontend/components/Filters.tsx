'use client';

import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';

const UNIVERSITIES = [
  "MIT",
  "Stanford",
  "CMU",
  "UC Berkeley",
  "UIUC",
  "Cornell",
  "UW",
  "Georgia Tech",
  "Princeton",
  "UT Austin",
];

interface FiltersProps {
  minHIndex: number;
  setMinHIndex: (value: number) => void;
  resultCount: number;
  setResultCount: (value: number) => void;
  universities: string[];
  setUniversities: (value: string[]) => void;
}

export function Filters({
  minHIndex,
  setMinHIndex,
  resultCount,
  setResultCount,
  universities,
  setUniversities,
}: FiltersProps) {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <Label
            className="text-sm cursor-help"
            title="H-index measures a researcher's productivity and citation impact. An H-index of N means N papers with at least N citations each."
          >
            Minimum H-Index: {minHIndex}
          </Label>
          <Slider
            value={[minHIndex]}
            onValueChange={(v) => setMinHIndex(v[0])}
            min={0}
            max={100}
            step={5}
            className="mt-2"
          />
        </div>
        <div>
          <Label className="text-sm">Results: {resultCount}</Label>
          <Slider
            value={[resultCount]}
            onValueChange={(v) => setResultCount(v[0])}
            min={5}
            max={20}
            step={5}
            className="mt-2"
          />
        </div>
      </div>
      <div className="space-y-2">
        <Label className="text-sm">Universities</Label>
        <div className="flex flex-wrap gap-2">
          {UNIVERSITIES.map((uni) => (
            <button
              key={uni}
              type="button"
              onClick={() => {
                if (universities.includes(uni)) {
                  setUniversities(universities.filter((u) => u !== uni));
                } else {
                  setUniversities([...universities, uni]);
                }
              }}
              className={`px-3 py-1 text-sm rounded-full border transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ${
                universities.includes(uni)
                  ? "bg-primary text-primary-foreground border-primary"
                  : "bg-background hover:bg-muted border-input"
              }`}
            >
              {uni}
            </button>
          ))}
        </div>
        {universities.length > 0 && (
          <button
            type="button"
            onClick={() => setUniversities([])}
            className="text-xs text-muted-foreground hover:underline"
          >
            Clear all
          </button>
        )}
      </div>
    </div>
  );
}
