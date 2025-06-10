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

  // Example configurations
  const examples = [
    {
      id: "example-1",
      name: "3-Tier Architecture",
      description: "Simple web application with frontend, backend, and database",
      file: "/examples/example-1.py"
    },
    {
      id: "example-2", 
      name: "Microservices",
      description: "Microservices architecture with API gateway and multiple services",
      file: "/examples/example-2.py"
    },
    {
      id: "example-3",
      name: "Serverless",
      description: "Serverless web application using AWS Lambda and DynamoDB",
      file: "/examples/example-3.py"
    },
    {
      id: "example-4",
      name: "Kubernetes",
      description: "Kubernetes deployment with pods, services, and ingress",
      file: "/examples/example-4.py"
    }
  ];

  let selectedExample = examples[0].id;
  let code = "";
  let previewLoading = false;
  let error = "";

  // Function to load example code from file
  async function loadExample(exampleId: string) {
    const example = examples.find(ex => ex.id === exampleId);
    if (!example) return;

    try {
      const response = await fetch(example.file);
      if (response.ok) {
        code = await response.text();
      } else {
        error = `Failed to load example: ${response.status}`;
      }
    } catch (err) {
      error = `Failed to load example: ${err instanceof Error ? err.message : "Unknown error"}`;
    }
  }

  // Function to handle example selection
  async function handleExampleChange(exampleId: string) {
    selectedExample = exampleId;
    await loadExample(selectedExample);
  }

  // Function to handle code changes
  function handleCodeChange(newCode: string) {
    code = newCode;
  }

  // Function to handle manual generation (for header button)
  function handleGenerate() {
    // The Preview component handles generation automatically with debouncing
    // This function can be used for manual triggers if needed
  }

  // Load initial example on component mount
  onMount(() => {
    loadExample(selectedExample);
  });
</script>

<main class="h-screen flex flex-col bg-background">
  <!-- Header -->
  <Header 
    {examples}
    {selectedExample}
    isLoading={previewLoading}
    onExampleChange={handleExampleChange}
    onGenerate={handleGenerate}
  />

  <!-- Main Content Area with Resizable Panes -->
  <div class="flex-1 overflow-hidden">
    <ResizablePaneGroup direction="horizontal" class="h-full">
      <!-- Left Pane - Code Editor -->
      <ResizablePane defaultSize={50} minSize={30}>
        <CodeEditor 
          {code}
          onCodeChange={handleCodeChange}
        />
      </ResizablePane>

      <ResizableHandle withHandle />

      <!-- Right Pane - Diagram Preview -->
      <ResizablePane defaultSize={50} minSize={30}>
        <Preview {code} bind:isLoading={previewLoading} />
      </ResizablePane>
    </ResizablePaneGroup>
  </div>
</main>
