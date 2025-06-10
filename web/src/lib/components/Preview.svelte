<script lang="ts">
  import { onDestroy } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import {
    Alert,
    AlertDescription,
    AlertTitle,
  } from "$lib/components/ui/alert";
  import { Play, Image, AlertCircle } from "@lucide/svelte";
  import { getDiagramPreview } from "$lib/net/api";

  export let code: string;

  let diagramUrl = "";
  let isLoading = false;
  let error = "";
  let debounceTimer: NodeJS.Timeout | null = null;

  // Export loading state for parent components
  export { isLoading };

  // Debounce delay in milliseconds
  const DEBOUNCE_DELAY = 500;

  // Function to generate diagram from Python code
  async function generateDiagram() {
    if (!code.trim()) {
      diagramUrl = "";
      return;
    }

    isLoading = true;
    error = "";

    try {
      const result = await getDiagramPreview(code);
      
      if (result.type === "success" && result.blob) {
        // Clean up previous URL to prevent memory leaks
        if (diagramUrl) {
          URL.revokeObjectURL(diagramUrl);
        }
        diagramUrl = URL.createObjectURL(result.blob);
      } else {
        error = result.error || "Unknown error occurred";
        diagramUrl = "";
      }
    } catch (err) {
      error = `Failed to generate diagram: ${err instanceof Error ? err.message : "Unknown error"}`;
      diagramUrl = "";
    } finally {
      isLoading = false;
    }
  }

  // Debounced function to generate diagram
  function debouncedGenerateDiagram() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    
    debounceTimer = setTimeout(() => {
      generateDiagram();
    }, DEBOUNCE_DELAY);
  }

  // Watch for code changes and trigger debounced generation
  $: if (code !== undefined) {
    debouncedGenerateDiagram();
  }

  // Cleanup on component destroy
  onDestroy(() => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    if (diagramUrl) {
      URL.revokeObjectURL(diagramUrl);
    }
  });

  // Manual generate function for the button
  function handleManualGenerate() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    generateDiagram();
  }
</script>

<div class="h-full flex flex-col">
  <!-- Diagram Header -->
  <div class="border-b bg-muted/50 px-4 py-3 flex items-center gap-2">
    <Image class="h-4 w-4 text-muted-foreground" />
    <h2 class="font-semibold text-foreground">Generated Diagram</h2>
  </div>

  <!-- Diagram Content -->
  <div class="flex-1 p-4 flex items-center justify-center bg-muted/10">
    {#if isLoading}
      <div class="flex flex-col items-center space-y-4">
        <div
          class="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent"
        ></div>
        <p class="text-sm text-muted-foreground">
          Generating diagram...
        </p>
      </div>
    {:else if error}
      <div class="max-w-md w-full">
        <Alert variant="destructive">
          <AlertCircle class="h-4 w-4" />
          <AlertTitle>Error generating diagram</AlertTitle>
          <AlertDescription class="mt-2">
            {error}
          </AlertDescription>
        </Alert>
        <div class="mt-4 flex justify-center">
          <Button
            variant="outline"
            onclick={handleManualGenerate}
            class="gap-2"
          >
            <Play class="h-4 w-4" />
            Try Again
          </Button>
        </div>
      </div>
    {:else if diagramUrl}
      <div class="max-w-full max-h-full overflow-auto">
        <img
          src={diagramUrl}
          alt="Generated Diagram"
          class="max-w-full max-h-full object-contain rounded-lg border shadow-sm"
          onerror={() => {
            error = "Failed to load generated diagram";
          }}
        />
      </div>
    {:else}
      <div class="text-center text-muted-foreground">
        <div class="mx-auto h-12 w-12 text-muted-foreground/50 mb-4">
          <svg
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            class="w-full h-full"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v14a2 2 0 002 2z"
            />
          </svg>
        </div>
        <p class="text-sm">Write Python code to generate a diagram</p>
        <p class="text-xs mt-1 text-muted-foreground/70">
          Your diagram will appear here
        </p>
      </div>
    {/if}
  </div>

  <!-- Diagram Footer -->
  <div class="border-t bg-muted/30 p-4">
    <div class="flex items-center gap-2 text-sm">
      {#if diagramUrl}
        <div class="flex items-center gap-2 text-green-600">
          <div class="w-2 h-2 bg-green-500 rounded-full"></div>
          <span>Diagram generated successfully</span>
        </div>
      {:else if error}
        <div class="flex items-center gap-2 text-destructive">
          <div class="w-2 h-2 bg-destructive rounded-full"></div>
          <span>Generation failed</span>
        </div>
      {:else if isLoading}
        <div class="flex items-center gap-2 text-blue-600">
          <div
            class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"
          ></div>
          <span>Generating diagram...</span>
        </div>
      {:else if code.trim()}
        <div class="flex items-center gap-2 text-muted-foreground">
          <div class="w-2 h-2 bg-muted-foreground rounded-full"></div>
          <span>Ready to generate</span>
        </div>
      {:else}
        <div class="flex items-center gap-2 text-muted-foreground">
          <div
            class="w-2 h-2 bg-muted-foreground/50 rounded-full"
          ></div>
          <span>Enter code to get started</span>
        </div>
      {/if}
    </div>
  </div>
</div> 