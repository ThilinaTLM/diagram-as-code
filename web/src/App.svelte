<script lang="ts">
  import { onMount } from "svelte";
  import {
    ResizableHandle,
    ResizablePane,
    ResizablePaneGroup,
  } from "$lib/components/ui/resizable";
  import Header from "$lib/components/Header.svelte";
  import CodeEditor from "$lib/components/CodeEditor.svelte";
  import Preview from "$lib/components/Preview.svelte";

  const examples = [
    {
      id: "example-1",
      name: "3-Tier Architecture",
      description:
        "Simple web application with frontend, backend, and database",
      file: "/examples/example-1.py",
    },
    {
      id: "example-2",
      name: "Microservices",
      description:
        "Microservices architecture with API gateway and multiple services",
      file: "/examples/example-2.py",
    },
    {
      id: "example-3",
      name: "Serverless",
      description: "Serverless web application using AWS Lambda and DynamoDB",
      file: "/examples/example-3.py",
    },
    {
      id: "example-4",
      name: "Kubernetes",
      description: "Kubernetes deployment with pods, services, and ingress",
      file: "/examples/example-4.py",
    },
  ];

  let selectedExample = $state(examples[0].id);
  let code = $state("");
  let error = $state("");

  function encodeCodeToBase64(code: string): string {
    try {
      return btoa(unescape(encodeURIComponent(code)));
    } catch (err) {
      console.error("Failed to encode code:", err);
      return "";
    }
  }

  function decodeCodeFromBase64(base64: string): string {
    try {
      return decodeURIComponent(escape(atob(base64)));
    } catch (err) {
      console.error("Failed to decode code:", err);
      return "";
    }
  }

  function updateURL(code: string) {
    if (typeof window === "undefined") return;

    const url = new URL(window.location.href);
    if (code.trim()) {
      const encodedCode = encodeCodeToBase64(code);
      url.searchParams.set("code", encodedCode);
    } else {
      url.searchParams.delete("code");
    }

    window.history.replaceState({}, "", url.toString());
  }

  function loadCodeFromURL(): string | null {
    if (typeof window === "undefined") return null;

    const params = new URLSearchParams(window.location.search);
    const encodedCode = params.get("code");

    if (encodedCode) {
      return decodeCodeFromBase64(encodedCode);
    }

    return null;
  }

  async function loadExample(exampleId: string) {
    const example = examples.find((ex) => ex.id === exampleId);
    if (!example) return;

    try {
      const response = await fetch(example.file);
      if (response.ok) {
        const exampleCode = await response.text();
        code = exampleCode;
        updateURL(code);
      } else {
        error = `Failed to load example: ${response.status}`;
      }
    } catch (err) {
      error = `Failed to load example: ${err instanceof Error ? err.message : "Unknown error"}`;
    }
  }

  async function handleExampleChange(exampleId: string) {
    selectedExample = exampleId;

    if (exampleId !== "custom") {
      await loadExample(selectedExample);
    }
  }

  function handleCodeChange(newCode: string) {
    code = newCode;
    updateURL(code);

    if (selectedExample !== "custom" && code !== newCode) {
      selectedExample = "custom";
    }
  }

  onMount(() => {
    const urlCode = loadCodeFromURL();

    if (urlCode) {
      code = urlCode;
      selectedExample = "custom";
    } else {
      loadExample(selectedExample);
    }
  });
</script>

<main class="h-screen flex flex-col bg-background">
  <Header {examples} {selectedExample} onExampleChange={handleExampleChange} />

  <div class="flex-1 overflow-hidden">
    <ResizablePaneGroup direction="horizontal" class="h-full">
      <ResizablePane defaultSize={50} minSize={30}>
        <CodeEditor {code} onCodeChange={handleCodeChange} />
      </ResizablePane>

      <ResizableHandle withHandle />

      <ResizablePane defaultSize={50} minSize={30}>
        <Preview {code} />
      </ResizablePane>
    </ResizablePaneGroup>
  </div>
</main>
