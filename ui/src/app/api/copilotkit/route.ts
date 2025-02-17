import { NextRequest, NextResponse } from "next/server";
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import OpenAI from "openai";

// Constants
const REMOTE_ACTION_URL = process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit";
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

let runtime: CopilotRuntime | null = null;
let serviceAdapter: OpenAIAdapter | null = null;

if (OPENAI_API_KEY) {
  const openai = new OpenAI({
    apiKey: OPENAI_API_KEY,
  });

  serviceAdapter = new OpenAIAdapter({ openai });
  runtime = new CopilotRuntime({
    remoteEndpoints: [
      {
        url: REMOTE_ACTION_URL,
      },
    ],
  });
}

export async function POST(req: NextRequest) {
  if (!runtime || !serviceAdapter) {
    console.error("OPENAI_API_KEY is required but not set in environment variables");
    return NextResponse.json(
      { error: "OpenAI API Key not configured" },
      { status: 500 }
    );
  }

  try {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: "/api/copilotkit",
    });

    return handleRequest(req);
  } catch (error) {
    console.error("Error processing copilotkit request:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
} 