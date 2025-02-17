'use client';

import { CopilotKit, useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { BlogPost } from "@/components/blog-post";
import { ErrorBoundary } from "@/components/error-boundary";
import { type AgentState, type BlogPost as BlogPostType } from "@/types/blog";
import { THEME } from "@/styles/theme";
import initialState from "./initial-state.json";

// Helper to parse blog post from repr string
const parseBlogPost = (repr: string): BlogPostType | null => {
  try {
    const match = repr.match(/BlogPost\(title='([^']*)', content="([^"]*)"\)/);
    if (match) {
      return {
        title: match[1],
        content: match[2].replace(/\\n/g, '\n')
      };
    }
    return null;
  } catch (error) {
    console.error('Error parsing blog post:', error);
    return null;
  }
};

function MainContent() {
  const { state } = useCoAgent<AgentState>({
    name: "blog-post-generator",
    initialState: initialState
  });

  // Parse blog post from repr if available
  const blogPost = state?.blog_post && (state.blog_post as BlogPostType & { repr?: string }).repr 
    ? parseBlogPost((state.blog_post as BlogPostType & { repr: string }).repr) 
    : null;

  return (
    <div 
      className="flex w-full h-screen overflow-hidden"
      style={{ backgroundColor: THEME.colors.background }}
    >
      {/* Main content area */}
      <div className="flex-1 overflow-y-auto p-4 mr-[400px]">
        {blogPost && (
          <div className="max-w-4xl mx-auto">
            <BlogPost 
              title={blogPost.title}
              content={blogPost.content}
              className="mb-8"
            />
          </div>
        )}
      </div>

      {/* Right sidebar with chat */}
      <div 
        className="w-[400px] h-screen flex flex-col border-l shrink-0 fixed right-0 top-0"
        style={{ borderColor: THEME.colors.border, backgroundColor: THEME.colors.background }}
      >
        <CopilotChat
          labels={{
            title: "Blog Post Generator",
            initial: "How can I help you generate blog posts today?"
          }}
          instructions="I am a blog post generation assistant. I can help you create engaging blog content."
          className="h-full"
        />
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <main className="min-h-screen">
      <ErrorBoundary>
        <CopilotKit runtimeUrl="/api/copilotkit" agent="blog-post-generator" showDevConsole={false}>
          <MainContent />
        </CopilotKit>
      </ErrorBoundary>
    </main>
  );
}

