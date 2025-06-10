<script lang="ts">
  let code = `with Diagram("Simple 3-Tier Architecture"):
    users = Users("Users")
    
    with Cluster("Frontend"):
        web = Nginx("Web Server")
    
    with Cluster("Backend"):
        api = EC2("API Server")
    
    with Cluster("Database"):
        db = PostgreSQL("Database")
    
    users >> web >> api >> db`;
  
  let diagramUrl = "";
  let isLoading = false;
  let error = "";
  
  // Function to handle code changes and generate diagram
  async function handleCodeChange(event: Event) {
    const target = event.target as HTMLTextAreaElement;
    code = target.value;
    await generateDiagram();
  }
  
  // Function to generate diagram from Python code
  async function generateDiagram() {
    if (!code.trim()) {
      diagramUrl = "";
      return;
    }
    
    isLoading = true;
    error = "";
    
    try {
      const response = await fetch('http://localhost:5000/diagram', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
        },
        body: code
      });
      
      if (response.ok) {
        const blob = await response.blob();
        diagramUrl = URL.createObjectURL(blob);
      } else {
        throw new Error(`Server error: ${response.status}`);
      }
    } catch (err) {
      error = `Failed to generate diagram: ${err instanceof Error ? err.message : 'Unknown error'}`;
      diagramUrl = "";
    } finally {
      isLoading = false;
    }
  }
  
  // Generate initial diagram on component mount
  import { onMount } from 'svelte';
  onMount(() => {
    generateDiagram();
  });
</script>

<main class="h-screen flex flex-col">
  <!-- Header -->
  <header class="bg-gray-900 text-white p-4 shadow-lg">
    <h1 class="text-2xl font-bold">Python Graphviz Code Editor</h1>
    <p class="text-sm text-gray-300 mt-1">Write Python code using diagrams library to generate infrastructure diagrams</p>
  </header>
  
  <!-- Main Content Area -->
  <div class="flex-1 flex">
    <!-- Left Side - Code Editor -->
    <div class="w-1/2 flex flex-col bg-gray-100 border-r border-gray-300">
      <div class="bg-gray-800 text-white p-3 flex justify-between items-center">
        <h2 class="text-lg font-semibold">Python Code Editor</h2>
        <button
          class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
          on:click={generateDiagram}
          disabled={isLoading}
        >
          {isLoading ? 'Generating...' : 'Generate Diagram'}
        </button>
      </div>
      <div class="flex-1 p-4">
        <textarea
          class="w-full h-full resize-none border border-gray-300 rounded-lg p-4 font-mono text-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Write your Python diagrams code here..."
          bind:value={code}
          on:input={handleCodeChange}
        ></textarea>
      </div>
      <div class="p-4 bg-gray-50 border-t border-gray-300">
        <div class="text-xs text-gray-600 space-y-1">
          <p><strong>Example:</strong> Use the diagrams library syntax</p>
          <p>• Start with: <code class="bg-gray-200 px-1 rounded">with Diagram("Title"):</code></p>
          <p>• Create components: <code class="bg-gray-200 px-1 rounded">web = Nginx("Web Server")</code></p>
          <p>• Connect them: <code class="bg-gray-200 px-1 rounded">users >> web >> api</code></p>
        </div>
      </div>
    </div>
    
    <!-- Right Side - Diagram Preview -->
    <div class="w-1/2 flex flex-col bg-white">
      <div class="bg-gray-800 text-white p-3">
        <h2 class="text-lg font-semibold">Generated Diagram</h2>
      </div>
      <div class="flex-1 p-4 flex items-center justify-center">
        {#if isLoading}
          <div class="flex flex-col items-center space-y-4">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p class="text-gray-600">Generating diagram...</p>
          </div>
        {:else if error}
          <div class="text-center p-6 bg-red-50 rounded-lg border border-red-200">
            <div class="text-red-600 mb-2">
              <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-red-800 mb-2">Error</h3>
            <p class="text-sm text-red-700">{error}</p>
            <button
              class="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded transition-colors"
              on:click={generateDiagram}
            >
              Try Again
            </button>
          </div>
        {:else if diagramUrl}
          <div class="max-w-full max-h-full">
            <img
              src={diagramUrl}
              alt="Generated Diagram"
              class="max-w-full max-h-full object-contain rounded-lg shadow-lg"
              on:error={() => {
                error = "Failed to load generated diagram";
              }}
            />
          </div>
        {:else}
          <div class="text-center text-gray-500">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            <p class="mt-2">Write Python code to generate a diagram</p>
          </div>
        {/if}
      </div>
      <div class="p-4 bg-gray-50 border-t border-gray-300">
        <p class="text-sm text-gray-600">
          {#if diagramUrl}
            ✅ Diagram generated successfully
          {:else if code.trim()}
            ⏳ Write code and click "Generate Diagram" to see the result
          {:else}
            💡 Enter Python code using the diagrams library
          {/if}
        </p>
      </div>
    </div>
  </div>
</main>

<style>
  /* Custom scrollbar for textarea */
  textarea::-webkit-scrollbar {
    width: 8px;
  }
  
  textarea::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }
  
  textarea::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
  }
  
  textarea::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
  }
</style>
