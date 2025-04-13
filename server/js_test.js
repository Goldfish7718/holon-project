// import process from "process";

const prompt = "Explain the growth of Apple Inc.";

fetch("http://localhost:8000/chat/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ prompt }),
})
  .then((response) => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let fullText = "";

    function readChunk() {
      return reader.read().then(({ done, value }) => {
        if (done) {
          return;
        }

        const chunk = decoder.decode(value, { stream: true });
        fullText += chunk;

        // Do something with the chunk
        process.stdout.write(chunk); // or append to UI

        // Read next chunk
        return readChunk();
      });
    }

    return readChunk();
  })
  .catch((error) => {
    console.error("Error while streaming:", error);
  });
