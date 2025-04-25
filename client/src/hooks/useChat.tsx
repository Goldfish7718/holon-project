import { API_URL } from "@/App";
import { useState } from "react";

type StreamingResponseProps = {
  prompt: string;
  language?: string;
};

type UseChatReturns = {
  response: string;
  error: string | null;
  isTyping: boolean;
  getStreamingResponse: (props: StreamingResponseProps) => Promise<void>;
};

export default function useChat(): UseChatReturns {
  const [response, setResponse] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isTyping, setIsTyping] = useState(false);

  const getStreamingResponse = async ({
    prompt,
    language,
  }: StreamingResponseProps) => {
    const body = {
      prompt,
      language: language ? language : "en",
    };

    setResponse("");
    setError(null);
    setIsTyping(true);

    try {
      const response = await fetch(`${API_URL}/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("Response body is null");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let accumulatedResponse = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        if (chunk) {
          accumulatedResponse += chunk;
          setResponse(accumulatedResponse);
        }
      }
    } catch (error) {
      console.error("Error while streaming:", error);
      setError(error instanceof Error ? error.message : "An unknown error occurred");
    } finally {
      setIsTyping(false);
    }
  };

  return {
    response,
    error,
    isTyping,
    getStreamingResponse,
  };
}
