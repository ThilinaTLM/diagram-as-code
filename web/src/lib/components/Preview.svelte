<script lang="ts">
  import { onDestroy } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import {
    Alert,
    AlertDescription,
    AlertTitle,
  } from "$lib/components/ui/alert";
  import { Play, AlertCircle, RefreshCw, Download, ToggleLeft, ToggleRight } from "@lucide/svelte";
  import { getDiagramPreview } from "$lib/net/api";
  import DiagramViewer from "./DiagramViewer.svelte";

  interface Props {
    code: string;
  }

  let { code }: Props = $props();

  let diagramUrl = $state("");
  let isLoading = $state(false);
  let error = $state("");
  let debounceTimer: NodeJS.Timeout | null = $state(null);
  let autoRefresh = $state(true);

  const DEBOUNCE_DELAY = 500;

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

  function debouncedGenerateDiagram() {
    if (!autoRefresh) return;
    
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    debounceTimer = setTimeout(() => {
      generateDiagram();
    }, DEBOUNCE_DELAY);
  }

  let previousCode = $state(code);

  $effect(() => {
    if (code !== previousCode) {
      previousCode = code;
      if (code !== undefined) {
        debouncedGenerateDiagram();
      }
    }
  });

  onDestroy(() => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    if (diagramUrl) {
      URL.revokeObjectURL(diagramUrl);
    }
  });

  function handleManualGenerate() {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    generateDiagram();
  }

  function toggleAutoRefresh() {
    autoRefresh = !autoRefresh;
  }

  async function handleSaveImage() {
    if (!diagramUrl) return;

    try {
      const response = await fetch(diagramUrl);
      const blob = await response.blob();
      
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `diagram-${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    } catch (err) {
      console.error('Failed to save image:', err);
    }
  }
</script>

<div class="h-full flex flex-col">
  <!-- Toolbar -->
  <div class="flex items-center justify-between p-2 border-b bg-background/50 backdrop-blur-sm">
    <div class="flex items-center gap-2">
      <Button
        variant="ghost"
        size="sm"
        onclick={toggleAutoRefresh}
        class="gap-2 text-xs"
        title={autoRefresh ? "Disable auto-refresh" : "Enable auto-refresh"}
      >
        {#if autoRefresh}
          <ToggleRight class="h-3 w-3 text-green-600" />
        {:else}
          <ToggleLeft class="h-3 w-3 text-muted-foreground" />
        {/if}
        Auto
      </Button>
      
      <Button
        variant="ghost"
        size="sm"
        onclick={handleManualGenerate}
        disabled={isLoading}
        class="gap-2 text-xs"
        title="Refresh diagram"
      >
        <RefreshCw class={`h-3 w-3 ${isLoading ? 'animate-spin' : ''}`} />
        Refresh
      </Button>
    </div>

    <Button
      variant="ghost"
      size="sm"
      onclick={handleSaveImage}
      disabled={!diagramUrl || isLoading}
      class="gap-2 text-xs"
      title="Save diagram as image"
    >
      <Download class="h-3 w-3" />
      Save
    </Button>
  </div>

  <!-- Main content area -->
  <div class="flex-1 flex items-center justify-center bg-muted/10">
    {#if isLoading}
      <div class="flex flex-col items-center space-y-4">
        <div
          class="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent"
        ></div>
        <p class="text-sm text-muted-foreground">Generating diagram...</p>
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
      <DiagramViewer
        src={diagramUrl}
        alt="Generated Diagram"
        class="shadow-sm"
      />
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
</div>
