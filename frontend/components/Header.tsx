import Link from 'next/link';

type HeaderProps = {
  currentPage: 'search' | 'explore' | 'resources';
};

export function Header({ currentPage }: HeaderProps) {
  const navItems = [
    { key: 'search', href: '/', label: 'Search' },
    { key: 'explore', href: '/explore', label: 'Explore' },
    { key: 'resources', href: '/resources', label: 'Resources' },
  ] as const;

  return (
    <div className="border-b bg-white sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="text-lg font-semibold tracking-tight hover:opacity-80 transition-opacity">
          Research Advisor Finder
        </Link>
        <nav className="flex items-center gap-1">
          {navItems.map((item) => (
            <Link
              key={item.key}
              href={item.href}
              className={`text-sm px-3 py-1.5 rounded-md transition-colors ${
                currentPage === item.key
                  ? 'font-medium text-foreground bg-slate-100'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </div>
  );
}
