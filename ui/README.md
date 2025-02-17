# Blog Post Generator

A modern web application built with Next.js that helps users generate engaging blog content using AI assistance. The project leverages CopilotKit for AI-powered content generation and features a clean, responsive interface.

## Features

- 🤖 AI-powered blog post generation
- 💻 Real-time content preview
- 🎨 Modern UI with Shadcn UI and Tailwind CSS
- 🌙 Dark mode support
- ⚡ Built with Next.js App Router and TypeScript
- 🔄 State management with CopilotKit
- 📱 Responsive design for all devices

## Tech Stack

- **Framework:** Next.js 15 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS, Shadcn UI
- **AI Integration:** CopilotKit
- **Package Manager:** pnpm
- **UI Components:** Radix UI
- **Markdown:** React Markdown with syntax highlighting
- **Development:** Turbopack for fast refresh

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Set up your environment variables:
   Create a `.env.local` file in the root directory with your API keys.
   OPENAI_API_KEY=
   REMOTE_ACTION_URL=http://localhost:8000/copilotkit  

4. Run the development server:
   ```bash
   pnpm dev
   ```

   The application will start using Turbopack for faster development experience.

5. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

```
src/
├── app/              # Next.js App Router pages
├── components/       # Reusable UI components
├── types/           # TypeScript type definitions
└── styles/          # Global styles and theme
```

## Development

- The main page is in `src/app/page.tsx`
- Blog post components are in `src/components/blog-post.tsx`
- Type definitions are in `src/types/blog.ts`
- Theme configuration is in `src/styles/theme.ts`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
