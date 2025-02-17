export interface BlogPost {
  title: string;
  content: string;
  repr?: string;
  lc?: number;
  type?: string;
  id?: string[];
}

export interface SearchResults {
  query: string;
  results: string[];
}

export interface AgentState {
  messages: Array<{
    content: string;
    role?: string;
    id?: string;
  }>;
  blog_post: BlogPost;
  route: string | null;
  search_results: SearchResults;
} 