'use client';

import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';

interface FiltersProps {
  minHIndex: number;
  setMinHIndex: (value: number) => void;
  resultCount: number;
  setResultCount: (value: number) => void;
}
