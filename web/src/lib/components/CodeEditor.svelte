<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import * as monaco from "monaco-editor";

  let { code, onCodeChange } = $props();

  let editorContainer: HTMLDivElement | null = $state(null);
  let editor: monaco.editor.IStandaloneCodeEditor | null = null;
  let isInitialized = $state(false);
  let isLoading = $state(false);
  let hasError = $state(false);

  onMount(async () => {
    if (!editorContainer) return;

    try {
      isLoading = true;

      editor = monaco.editor.create(editorContainer, {
        value: code,
        language: "python",
        theme: "vs",
        automaticLayout: true,
        minimap: { enabled: true },
        scrollBeyondLastLine: false,
        fontSize: 14,
        fontFamily:
          'JetBrains Mono, Consolas, Monaco, "Courier New", monospace',
        lineNumbers: "on",
        renderWhitespace: "selection",
        tabSize: 4,
        insertSpaces: true,
        wordWrap: "on",
        bracketPairColorization: { enabled: true },
        guides: {
          indentation: true,
          bracketPairs: true,
        },
        suggest: {
          showKeywords: true,
          showSnippets: true,
        },
      });

      editor.onDidChangeModelContent(() => {
        if (editor && isInitialized) {
          const newCode = editor.getValue();
          if (newCode !== code) {
            onCodeChange(newCode);
          }
        }
      });

      isInitialized = true;
      isLoading = false;
    } catch (error) {
      console.error("Failed to initialize Monaco Editor:", error);
      hasError = true;
      isLoading = false;
    }
  });

  onDestroy(() => {
    if (editor) {
      editor.dispose();
      editor = null;
    }
  });

  $effect(() => {
    if (editor && isInitialized && code !== editor.getValue()) {
      const position = editor.getPosition();
      editor.setValue(code);
      if (position) {
        editor.setPosition(position);
      }
    }
  });
</script>

<div class="h-full flex flex-col">
  <div class="flex-1 relative py-6">
    {#if isLoading}
      <div class="w-full h-full flex items-center justify-center bg-background">
        <div class="text-muted-foreground">Loading Monaco Editor...</div>
      </div>
    {:else if hasError}
      <textarea
        class="w-full h-full resize-none border p-4 font-mono text-sm bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
        placeholder="Write your Python diagrams code here..."
        bind:value={code}
        oninput={(e) => onCodeChange((e.target as HTMLTextAreaElement).value)}
      ></textarea>
    {:else}
      <div
        bind:this={editorContainer}
        class="w-full h-full"
        style="min-height: 400px;"
      ></div>
    {/if}
  </div>
</div>

<style>
  :global(.monaco-editor) {
    --vscode-editor-background: hsl(var(--background));
    --vscode-editor-foreground: hsl(var(--foreground));
  }

  /* Custom styling for dark theme integration */
  :global(.monaco-editor .margin) {
    background-color: hsl(var(--background));
  }
</style>
