'use client';

import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';

interface FiltersProps {
  minHIndex: number;
  setMinHIndex: (value: number) => void;
  resultCount: number;
  setResultCount: (value: number) => void;
}
export function Filters({
  minHIndex,
  setMinHIndex,
  resultCount,
  setResultCount,
}: FiltersProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <div>
        <Label className="text-sm">Minimum H-Index: {minHIndex}</Label>
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
  );
}
