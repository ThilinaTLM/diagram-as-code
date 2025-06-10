<script lang="ts">
  import { Code } from "@lucide/svelte";

  export let code: string;
  export let selectedExample: string;
  export let examples: Array<{
    id: string;
    name: string;
    description: string;
    file: string;
  }>;
  export let onCodeChange: (code: string) => void;

  function handleCodeChange(event: Event) {
    const target = event.target as HTMLTextAreaElement;
    onCodeChange(target.value);
  }
</script>

<div class="h-full flex flex-col">
  <!-- Code Editor Header -->
  <div class="border-b bg-muted/50 px-4 py-3">
    <div class="flex items-center gap-2 mb-2">
      <Code class="h-4 w-4 text-muted-foreground" />
      <h2 class="font-semibold text-foreground">Python Code Editor</h2>
    </div>
    {#if selectedExample}
      {@const currentExample = examples.find(ex => ex.id === selectedExample)}
      {#if currentExample}
        <p class="text-xs text-muted-foreground">
          <span class="font-medium">{currentExample.name}:</span> {currentExample.description}
        </p>
      {/if}
    {/if}
  </div>

  <!-- Code Editor -->
  <div class="flex-1 p-4">
    <textarea
      class="w-full h-full resize-none border rounded-lg p-4 font-mono text-sm bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
      placeholder="Write your Python diagrams code here..."
      bind:value={code}
      oninput={handleCodeChange}
    ></textarea>
  </div>

  <!-- Code Editor Footer -->
  <div class="border-t bg-muted/30 p-4">
    <div class="text-xs text-muted-foreground space-y-2">
      <p class="font-medium">Quick Reference:</p>
      <div class="grid grid-cols-1 gap-1">
        <p>
          • Start with: <code
            class="bg-muted px-1.5 py-0.5 rounded text-xs"
            >with Diagram("Title"):</code
          >
        </p>
        <p>
          • Create components: <code
            class="bg-muted px-1.5 py-0.5 rounded text-xs"
            >web = Nginx("Web Server")</code
          >
        </p>
        <p>
          • Connect them: <code
            class="bg-muted px-1.5 py-0.5 rounded text-xs"
            >users >> web >> api</code
          >
        </p>
      </div>
    </div>
  </div>
</div>

<style>
  /* Custom scrollbar styling */
  textarea::-webkit-scrollbar {
    width: 8px;
  }

  textarea::-webkit-scrollbar-track {
    background: hsl(var(--muted));
    border-radius: 4px;
  }

  textarea::-webkit-scrollbar-thumb {
    background: hsl(var(--muted-foreground) / 0.3);
    border-radius: 4px;
  }

  textarea::-webkit-scrollbar-thumb:hover {
    background: hsl(var(--muted-foreground) / 0.5);
  }
</style> 