const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Paper {
  id: number;
  title: string;
  year: number | null;
  venue: string | null;
  citation_count: number | null;
}

export interface Faculty {
  id: number;
  name: string;
  affiliation: string | null;
  h_index: number | null;
  paper_count: number | null;
  semantic_scholar_id: string | null;
  research_tags: string[];
}

export interface SearchResult {
  faculty: Faculty;
  similarity: number;
  papers: Paper[];
}

export interface BreakdownItem {
  level: string; // High, Medium, Low
  reason: string;
}

export interface ExplanationBreakdown {
  topic_alignment?: BreakdownItem;
  paper_relevance?: BreakdownItem;
  research_fit?: BreakdownItem;
}

export interface ExplanationResponse {
  explanation: string;
  breakdown?: ExplanationBreakdown;
}

export async function searchFaculty(
  query: string,
  limit: number = 10,
  minHIndex: number = 0,
  universities: string[] = []
): Promise<SearchResult[]> {
  const response = await fetch(`${API_URL}/api/search/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      limit,
      min_h_index: minHIndex,
      universities: universities.length > 0 ? universities : null,
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
): Promise<ExplanationResponse> {
  const response = await fetch(`${API_URL}/api/search/explain`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      interests,
      faculty_id: facultyId,
    }),
  });

  if (!response.ok) {
    throw new Error("Explanation failed");
  }

  return response.json();
}

export interface CVUploadResponse {
  extracted_interests: string;
  results: SearchResult[];
}

export interface CVUploadParams {
  file: File;
  limit?: number;
  minHIndex?: number;
  universities?: string[];
}

export async function uploadCV(params: CVUploadParams): Promise<CVUploadResponse> {
  const formData = new FormData();
  formData.append('file', params.file);

  // Build query params
  const queryParams = new URLSearchParams();
  if (params.limit) queryParams.append('limit', params.limit.toString());
  if (params.minHIndex) queryParams.append('min_h_index', params.minHIndex.toString());
  if (params.universities) {
    params.universities.forEach(u => queryParams.append('universities', u));
  }

  const url = `${API_URL}/api/upload/cv?${queryParams.toString()}`;

  const response = await fetch(url, {
    method: 'POST',
    body: formData,
    // Note: Don't set Content-Type header - browser sets it with boundary for multipart
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to upload CV');
  }

  return response.json();
}
