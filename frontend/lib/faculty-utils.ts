export const MATCH_THRESHOLDS = {
  HIGH: 0.5,
  MEDIUM: 0.35,
} as const;

export const H_INDEX_THRESHOLDS = {
  JUNIOR: 30,
  RISING: 60,
} as const;

export function getMatchColor(similarity: number): string {
  if (similarity > MATCH_THRESHOLDS.HIGH) {
    return 'bg-green-100 text-green-800';
  }
  if (similarity > MATCH_THRESHOLDS.MEDIUM) {
    return 'bg-yellow-100 text-yellow-800';
  }
  return 'bg-slate-100 text-slate-800';
}

export function getFacultyBadge(hIndex: number | null): { label: string; className: string } | null {
  if (hIndex === null || hIndex === undefined) {
    return null;
  }
  if (hIndex < H_INDEX_THRESHOLDS.JUNIOR) {
    return { label: 'Junior Faculty', className: 'bg-orange-100 text-orange-800' };
  }
  if (hIndex > H_INDEX_THRESHOLDS.JUNIOR && hIndex < H_INDEX_THRESHOLDS.RISING) {
    return { label: 'Rising Junior Faculty', className: 'bg-yellow-100 text-yellow-800' };
  }
  if (hIndex > H_INDEX_THRESHOLDS.RISING) {
    return { label: 'Established Faculty', className: 'bg-green-100 text-green-800' };
  }
  return null;
}
