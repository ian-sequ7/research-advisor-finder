'use client';

import { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { SearchResult, getExplanation } from '@/lib/api';
import { ExternalLink, Loader2, Sparkles, FileText } from 'lucide-react';

interface ResultCardProps {
	result: SearchResult;
	rank: number;
	interests: string;
}
