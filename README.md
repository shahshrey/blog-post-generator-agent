# Blog Post Generator

A modern, AI-powered blog content generation system consisting of an intelligent agent for content creation and a sleek web interface. This project combines advanced LLM capabilities with a responsive UI to help users generate engaging blog content.

## 🌟 Key Features

- 🤖 AI-powered blog post generation with multi-step processing
- 🔍 Automated web research and content refinement
- 💻 Real-time content preview with modern UI
- 🎨 Clean, responsive interface with dark mode support
- 📱 Mobile-first design approach
- 🔄 Sophisticated state management
- ⚡ High-performance development setup

## 🏗️ System Architecture

The project consists of two main components:

### Agent Architecture
```mermaid
graph TD
    A[User Input] --> B[Router Node]
    B -->|Research Needed| C[Web Search Node]
    B -->|Generate Content| D[Generate Blog Node]
    B -->|Chat Response| E[Chat Node]
    C --> F[State Management]
    D --> F
    E --> F
    F -->|Feedback Loop| G[Feedback Node]
    G -->|Refinement| B
```

### Processing Flow
```mermaid
stateDiagram-v2
    [*] --> Initialize
    Initialize --> RouteRequest
    RouteRequest --> WebSearch: Research needed
    RouteRequest --> GenerateBlog: Direct generation
    RouteRequest --> Chat: Chat response
    WebSearch --> GenerateBlog
    GenerateBlog --> Feedback
    Feedback --> RouteRequest: Needs refinement
    Feedback --> [*]: Meets criteria
```

## 💻 Tech Stack

### UI Component
- **Framework:** Next.js 15 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS, Shadcn UI, Radix UI
- **State Management:** CopilotKit
- **Package Manager:** pnpm
- **Development:** Turbopack

### Agent Component
- **Language:** Python 3.9+
- **Framework:** LangGraph
- **Package Manager:** UV
- **Key Libraries:** LangChain, OpenAI

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- pnpm (for UI)
- UV (for Agent)

### UI Setup

1. Clone the repo and Navigate to the UI directory:
   ```bash
   git clone git@github.com:shahshrey/blog-post-generator-agent.git
   cd blog-post-generator-agent/ui
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Configure environment:
   Create `.env.local` with:
   ```
   OPENAI_API_KEY=your_key_here
   REMOTE_ACTION_URL=http://localhost:8000/copilotkit
   ```

4. Start development server:
   ```bash
   pnpm dev
   ```

### Agent Setup

1. Navigate to the agent directory:
   ```bash
   cd agent
   ```

2. Create and activate virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # Unix/macOS
   .venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Configure environment:
   Create `.env` with required API keys

5. Start the agent:
   ```bash
   poetry run app
   ```

## 📁 Project Structure

```
blog-post-generator/
├── ui/
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   │   ├── components/    # UI components
│   │   │   ├── types/        # TypeScript types
│   │   │   └── styles/       # Global styles
│   │   └── public/           # Static assets
│   └── public/           # Static assets
│
├── agent/
│   ├── src/
│   │   ├── nodes/        # Processing nodes
│   │   ├── state/        # State management
│   │   ├── schema/       # Data schemas
│   │   ├── utils/        # Utilities
│   │   └── graph/        # Graph configs
│   └── main.py          # Entry point
```

## 🛠️ Agent Components

### Processing Nodes
- **Router Node:** Determines processing path based on input
- **Web Search Node:** Performs research using search APIs
- **Generate Blog Node:** Creates content using LLMs
- **Feedback Node:** Evaluates and suggests improvements
- **Chat Node:** Handles direct user interactions

## 🔄 Development Workflow

1. Start both UI and Agent servers
2. Access the UI at http://localhost:3000
3. Input your blog topic
4. The system will:
   - Research relevant content
   - Generate initial draft
   - Refine based on feedback
   - Present final content

## 🤖 Prompt Engineering Approach

The prompt engineering strategy follows a systematic workflow:

1. **Query Analysis**
   - Break down user topics into discrete, searchable questions
   - Identify key research areas and knowledge gaps

2. **Research Phase**
   - Execute targeted web searches for each sub-question
   - Aggregate and validate information from multiple sources

3. **Content Generation**
   - Transform research into structured blog content
   - Apply Chain-of-Thought reasoning for logical flow
   - Segment prompts into clear sections (Context, Requirements, Examples)

4. **Iterative Refinement**
   - Collect user feedback on generated content
   - Implement targeted improvements based on feedback
   - Validate changes against original requirements

5. **Quality Assurance**
   - Use LLM-based evaluation to assess content quality
   - Verify alignment with user intent and requirements
   - Ensure factual accuracy and coherence

## 🧪 Testing

### Running Tests

Run the test using:
```bash
python test.py
```

### Test Coverage

The test covers:
- Blog post generation workflow
- Content validation and feedback
- State management

Key test cases:
- Generation with default prompts
- Custom topic generation
- Validation of generated content
- Error handling for API failures
- State persistence and recovery
- Edge cases in content processing

Testing Approach:
- LLM as judge, we can add a lot more validations
- Structured outputs validation
- We can incorporate pytest and parameterize the tests for different scenarios and different prompts as well

## Design Decisions
- CopilotKit chosen for maintaining shared state between frontend and agent components
- Next.js selected for LLM-friendly development and easier integration with Cursor
- Blog posts rendered only after full generation for simplified frontend state management
- Agent awareness of frontend state changes for effective user feedback processing
- Conversational chatbot interface for natural user interaction

## Edge Cases
- Router node analyzes user intent and directs requests to specialized nodes
- Single agent handles multiple use cases through router-based architecture
- Better separation of concerns and workflow control compared to React-style agent approach
- Enhanced handling of edge cases through specialized node processing

## 🌐 Deployed Version

Access the live demo at: https://blog-post-generator-indol.vercel.app/

Note: The deployed version might experience initial loading delays due to cold starts on the free tier of Vercel and Railway.

Example usage:
```bash
Send a message to the chatbot:
"Write a blog post on the topic of 'The impact of AI on the future of work'"
```

## 🔐 Environment Variables

### UI Environment (.env.local)
```bash
OPENAI_API_KEY=your_openai_api_key
REMOTE_ACTION_URL=http://localhost:8000/copilotkit
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Agent Environment (.env)
```bash
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_key
PORT=8000
```
