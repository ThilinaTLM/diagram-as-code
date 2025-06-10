<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Play, FileText } from "@lucide/svelte";

  export let examples: Array<{
    id: string;
    name: string;
    description: string;
    file: string;
  }>;
  export let selectedExample: string;
  export let isLoading: boolean;
  export let onExampleChange: (exampleId: string) => void;
  export let onGenerate: () => void;

  function handleExampleChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    onExampleChange(target.value);
  }
</script>

<header class="border-b bg-card px-6 py-4">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold text-foreground">Graph as Code</h1>
      <p class="text-sm text-muted-foreground mt-1">
        Create infrastructure diagrams using Python and the diagrams library
      </p>
    </div>
    <div class="flex items-center gap-4">
      <!-- Example Selector -->
      <div class="flex items-center gap-2">
        <FileText class="h-4 w-4 text-muted-foreground" />
        <select 
          bind:value={selectedExample}
          onchange={handleExampleChange}
          class="px-3 py-2 border rounded-lg bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
        >
          {#each examples as example}
            <option value={example.id}>{example.name}</option>
          {/each}
        </select>
      </div>
      <Button onclick={onGenerate} disabled={isLoading} class="gap-2">
        <Play class="h-4 w-4" />
        {isLoading ? "Generating..." : "Generate"}
      </Button>
    </div>
  </div>
</header> 