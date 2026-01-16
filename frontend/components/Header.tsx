import Link from 'next/link';
import { GraduationCap, Home, Compass, BookOpen } from 'lucide-react';

type HeaderProps = {
  currentPage: 'search' | 'explore' | 'resources';
};

export function Header({ currentPage }: HeaderProps) {
  return (
    <div className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <GraduationCap className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-semibold">Research Advisor Finder</h1>
        </div>
        <div className="flex items-center gap-4">
          {currentPage !== 'search' && (
            <Link
              href="/"
              className="text-sm text-muted-foreground hover:text-primary flex items-center gap-1"
            >
              <Home className="h-4 w-4" />
              Search
            </Link>
          )}
          {currentPage !== 'explore' && (
            <Link
              href="/explore"
              className="text-sm text-muted-foreground hover:text-primary flex items-center gap-1"
            >
              <Compass className="h-4 w-4" />
              Explore
            </Link>
          )}
          {currentPage !== 'resources' && (
            <Link
              href="/resources"
              className="text-sm text-muted-foreground hover:text-primary flex items-center gap-1"
            >
              <BookOpen className="h-4 w-4" />
              Resources
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
