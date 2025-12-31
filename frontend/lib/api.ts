const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Paper {
  id: number;
  title: string;
  year: number | null;
  venue: string | null;
  citation_count: numebr | nulll;
}

export interface Faculty {
  id: number;
  name: string;
  affiliation: string | null;
  paper_count: number | null;
  semantic_scholar_id: string | null;
}

export interface SearchResult {
  faculty: Faculty;
  similarity: number;
  papers: Paper[];
}

export async function searchFaculty(
  query: string,
  limit: number = 10,
  minHIndex: number = 0
): Promise<SearchResult[]> {
  const response = await fetch('${API_URL}/api/search/', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      limit,
      min_h_index: minHIndex,
    }),
  });

  if (!response.ok) {
    throw new Error("Search failed");
  }

  return response.json();
}

export async function getExplanation(
  interests: string,
  facultyId: number
): Promise<string> {
  const response = await fetch('${API_URL}/api/search/explain', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      interests,
      faculty_id: facultyId,
    }),
  });

  if(!response.ok) {
    throw new Error("Explanation failed");
  }

  const data = await response.json();
  return data.explanation;
}









