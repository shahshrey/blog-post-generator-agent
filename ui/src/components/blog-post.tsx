'use client'

import { type FC, useState, useCallback, type ChangeEvent, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import rehypePrism from 'rehype-prism-plus'
import remarkGfm from 'remark-gfm'
import { type BlogPost as BlogPostType } from '@/types/blog'
import { THEME } from '@/styles/theme'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Loader2 } from 'lucide-react'
import { toast } from 'sonner'

interface BlogPostProps extends BlogPostType {
  className?: string
  onSave?: (post: BlogPostType) => Promise<void> | void
}

export const BlogPost: FC<BlogPostProps> = ({ 
  title: initialTitle, 
  content: initialContent, 
  className = '',
  onSave 
}) => {
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [title, setTitle] = useState(initialTitle)
  const [content, setContent] = useState(initialContent)
  const [previewMode, setPreviewMode] = useState(false)

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd/Ctrl + S to save
      if ((e.metaKey || e.ctrlKey) && e.key === 's' && isEditing) {
        e.preventDefault()
        handleSave()
      }
      // Esc to cancel
      if (e.key === 'Escape' && isEditing) {
        e.preventDefault()
        handleCancel()
      }
      // Cmd/Ctrl + E to toggle edit mode
      if ((e.metaKey || e.ctrlKey) && e.key === 'e') {
        e.preventDefault()
        setIsEditing(prev => !prev)
      }
      // Cmd/Ctrl + P to toggle preview in edit mode
      if ((e.metaKey || e.ctrlKey) && e.key === 'p' && isEditing) {
        e.preventDefault()
        setPreviewMode(prev => !prev)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isEditing])

  const handleCancel = useCallback(() => {
    setTitle(initialTitle)
    setContent(initialContent)
    setIsEditing(false)
    setPreviewMode(false)
  }, [initialTitle, initialContent])

  const handleSave = useCallback(async () => {
    if (!title.trim()) {
      toast.error('Title cannot be empty')
      return
    }

    try {
      setIsSaving(true)
      if (onSave) {
        await onSave({ title, content })
      }
      setIsEditing(false)
      setPreviewMode(false)
      toast.success('Changes saved successfully')
    } catch (error) {
      toast.error('Failed to save changes')
      console.error('Save error:', error)
    } finally {
      setIsSaving(false)
    }
  }, [title, content, onSave])

  if (isEditing) {
    return (
      <div 
        className={`space-y-4 transition-all duration-200 ease-in-out ${className}`}
        style={{ 
          color: THEME.colors.text,
          backgroundColor: THEME.colors.background 
        }}
      >
        <div className="flex justify-between items-center mb-4">
          <Input
            value={title}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
            placeholder="Enter title..."
            className="text-2xl font-bold flex-1 mr-4"
            style={{ color: THEME.colors.text }}
          />
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => setPreviewMode(prev => !prev)}
              className="whitespace-nowrap"
            >
              {previewMode ? 'Edit Mode' : 'Preview'}
            </Button>
            <Button 
              onClick={handleSave} 
              disabled={isSaving || !title.trim()}
              className="whitespace-nowrap"
            >
              {isSaving ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                'Save'
              )}
            </Button>
            <Button 
              variant="outline" 
              onClick={handleCancel}
              className="whitespace-nowrap"
            >
              Cancel
            </Button>
          </div>
        </div>

        {previewMode ? (
          <div className="border rounded-lg p-4">
            <ReactMarkdown
              className="markdown-content"
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypePrism]}
            >
              {content}
            </ReactMarkdown>
          </div>
        ) : (
          <Textarea
            value={content}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setContent(e.target.value)}
            placeholder="Enter content in markdown..."
            className="min-h-[400px] font-mono"
            style={{ color: THEME.colors.text }}
          />
        )}

        <div className="text-sm text-muted-foreground">
          <p>Keyboard shortcuts:</p>
          <ul className="list-disc list-inside">
            <li>Save: Cmd/Ctrl + S</li>
            <li>Cancel: Esc</li>
            <li>Toggle Preview: Cmd/Ctrl + P</li>
          </ul>
        </div>
      </div>
    )
  }

  return (
    <article 
      className={`prose prose-lg max-w-none dark:prose-invert transition-all duration-200 ease-in-out ${className}`}
      style={{ 
        color: THEME.colors.text,
        backgroundColor: THEME.colors.background 
      }}
    >
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold m-0">{title}</h1>
        <Button 
          variant="outline"
          onClick={() => setIsEditing(true)}
        >
          Edit
        </Button>
      </div>
      <ReactMarkdown
        className="markdown-content"
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypePrism]}
      >
        {content}
      </ReactMarkdown>
    </article>
  )
} 