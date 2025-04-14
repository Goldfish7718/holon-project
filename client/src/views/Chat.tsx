import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import useChat from "@/hooks/useChat";
import { useState } from "react";

function Chat() {
  const [prompt, setPrompt] = useState("");
  const { response, getStreamingResponse } = useChat();

  const handlePromptSubmit = () => {
    getStreamingResponse({ prompt });
    setPrompt("");
  };

  return (
    <>
      <main className="m-4">
        <div className="flex flex-col gap-2">
          <Label>Prompt:</Label>
          <Input onChange={(e) => setPrompt(e.target.value)} value={prompt} />
        </div>
        <Button className="my-2" onClick={handlePromptSubmit}>
          Stream response
        </Button>
        <p>{response}</p>
      </main>
    </>
  );
}

export default Chat;
