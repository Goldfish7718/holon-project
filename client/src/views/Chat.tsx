import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import useChat from "@/hooks/useChat";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChatMessage } from "@/components/ChatMessage";
import { Toast, ToastProvider, ToastTitle, ToastViewport } from "@/components/ui/toast";
import { cn } from "@/lib/utils";

interface Message {
  content: string;
  isAI: boolean;
}

function Chat() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { response, error: chatError, isTyping, getStreamingResponse } = useChat();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (response) {
      setMessages(prev => {
        const lastMessage = prev[prev.length - 1];
        if (lastMessage && lastMessage.isAI) {
          return [...prev.slice(0, -1), { content: response, isAI: true }];
        }
        return [...prev, { content: response, isAI: true }];
      });
    }
  }, [response]);

  useEffect(() => {
    if (chatError) {
      setError(chatError);
    }
  }, [chatError]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handlePromptSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    
    // Add user message immediately
    setMessages(prev => [...prev, { content: prompt, isAI: false }]);

    try {
      await getStreamingResponse({ prompt });
    } catch (err) {
      setError("Failed to get response. Please try again.");
    } finally {
      setIsLoading(false);
      setPrompt("");
    }
  };

  return (
    <ToastProvider>
      <div className="flex flex-col h-screen bg-gray-900">
        <header className="bg-gray-800 p-4 text-white">
          <h1 className="text-2xl font-bold">AI Chat Assistant</h1>
        </header>

        <main className="flex-1 overflow-y-auto p-4">
          <div className="max-w-3xl mx-auto">
            <AnimatePresence>
              {messages.map((message, index) => (
                <ChatMessage 
                  key={index} 
                  content={message.content} 
                  isAI={message.isAI} 
                />
              ))}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </div>
        </main>

        <form 
          onSubmit={handlePromptSubmit}
          className={cn(
            "border-t border-gray-700 bg-gray-800 p-4",
            isLoading && "opacity-70"
          )}
        >
          <div className="max-w-3xl mx-auto flex gap-2">
            <Input
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 bg-gray-700 border-gray-600 text-white placeholder:text-gray-400"
            />
            <Button 
              type="submit" 
              disabled={isLoading || !prompt.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              {isLoading ? "Sending..." : "Send"}
            </Button>
          </div>
        </form>

        {error && (
          <Toast variant="destructive" className="absolute bottom-4 right-4">
            <ToastTitle>{error}</ToastTitle>
          </Toast>
        )}
        <ToastViewport />
      </div>
    </ToastProvider>
  );
}

export default Chat;
