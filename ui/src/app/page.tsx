'use client';

import { CopilotKit, useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { BlogPost } from "@/components/blog-post";
import { ErrorBoundary } from "@/components/error-boundary";
import { type AgentState } from "@/types/blog";
import { THEME } from "@/styles/theme";
import initialState from "./initial-state.json";

function MainContent() {
  const { state } = useCoAgent<AgentState>({
    name: "blog-post-generator",
    initialState: initialState
  });

  console.log(JSON.stringify(state, null, 2));

  return (
    <div 
      className="flex w-full h-screen overflow-hidden"
      style={{ backgroundColor: THEME.colors.background }}
    >
      {/* Main content area */}
      <div className="flex-1 overflow-y-auto p-4 mr-[400px]">
        {state?.blog_post && (
          <div className="max-w-4xl mx-auto">
            <BlogPost 
              title={state.blog_post.title}
              content={state.blog_post.content}
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
        <CopilotKit publicApiKey="ck_pub_fc9ab3f752f63a9fdad9698bc49fcf60" agent="blog-post-generator" showDevConsole={false}>
          <MainContent />
        </CopilotKit>
      </ErrorBoundary>
    </main>
  );
}

