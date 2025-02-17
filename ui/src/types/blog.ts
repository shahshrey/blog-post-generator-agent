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
  lc?: number;
  type?: string;
  id?: string[];
  repr?: string;
}

export interface Message {
  role: string;
  content: string;
  id: string;
}

export interface AgentState {
  messages: Message[];
  blog_post: BlogPost;
  route: string | null;
  search_results: SearchResults;
} 