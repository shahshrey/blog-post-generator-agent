'use client'

import { type FC } from 'react'
import { type AgentState } from '@/types/blog'
import { THEME } from '@/styles/theme'
import { BlogPost } from './blog-post'

interface StateDisplayProps {
  state?: AgentState
  status?: string
  nodeName?: string
  isEditing?: boolean
}

const parseBlogPost = (state: AgentState) => {
  if (!state.blog_post) return null
  
  try {
    // Extract title and content from the repr field
    const blogPostRepr = state.blog_post.repr
    if (typeof blogPostRepr !== 'string') return null

    // Parse the title and content from the repr string
    const titleMatch = blogPostRepr.match(/title='([^']*)'/)
    const contentMatch = blogPostRepr.match(/content="([^"]*)"/)

    if (!titleMatch || !contentMatch) return null

    return {
      title: titleMatch[1],
      content: contentMatch[1].replace(/\\n/g, '\n') // Replace escaped newlines
    }
  } catch (error) {
    console.error('Error parsing blog post:', error)
    return null
  }
}

export const StateDisplay: FC<StateDisplayProps> = ({ 
  state, 
  status, 
  nodeName,
  isEditing 
}) => {
  if (!state) return null

  const blogPost = state.blog_post ? parseBlogPost(state) : null

  return (
    <div className="space-y-4">
      {blogPost && (
        <BlogPost 
          title={blogPost.title} 
          content={blogPost.content}
          className="mb-8"
        />
      )}
      <div 
        className="fixed bottom-4 right-4 p-4 rounded-lg shadow-lg max-w-sm"
        style={{ 
          backgroundColor: THEME.colors.background,
          color: THEME.colors.text,
          border: `1px solid ${THEME.colors.border}`
        }}
      >
        <h3 className="text-sm font-semibold mb-2">Agent State</h3>
        {nodeName && (
          <p className="text-xs mb-2" style={{ color: THEME.colors.secondary }}>
            Node: {nodeName}
          </p>
        )}
        {status && (
          <p className="text-xs mb-2" style={{ color: THEME.colors.primary }}>
            Status: {status}
          </p>
        )}
        {isEditing && (
          <p className="text-xs mb-2" style={{ color: THEME.colors.primary }}>
            Currently Editing
          </p>
        )}
        <pre className="text-xs overflow-auto max-h-40">
          {JSON.stringify(state, null, 2)}
        </pre>
      </div>
    </div>
  )
} 