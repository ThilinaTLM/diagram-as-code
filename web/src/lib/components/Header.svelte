<script lang="ts">
  import * as Select from "$lib/components/ui/select/index.js";

  type Example = {
    id: string;
    name: string;
    description: string;
    file: string;
  };

  let {
    examples,
    onExampleChange,
    selectedExample,
  }: {
    examples: Array<Example>;
    onExampleChange: (exampleId: string) => void;
    selectedExample: string;
  } = $props();

  const triggerContent = $derived(
    examples.find((example) => example.id === selectedExample)?.name ??
      "Select an example"
  );

  function handleValueChange(value: string | undefined) {
    if (value) {
      onExampleChange(value);
    }
  }
</script>

<header class="border-b bg-card px-6 py-2">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-xl font-bold text-foreground">Graph as Code</h1>
      <p class="text-sm text-muted-foreground">
        Create infrastructure diagrams using Python and the diagrams library
      </p>
    </div>
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2">
        <Select.Root
          type="single"
          name="selectedExample"
          value={selectedExample}
          onValueChange={handleValueChange}
        >
          <Select.Trigger class="w-[200px]">
            {triggerContent}
          </Select.Trigger>
          <Select.Content>
            <Select.Group>
              <Select.Label>Examples</Select.Label>
              {#each examples as example (example.id)}
                <Select.Item value={example.id} label={example.name}>
                  {example.name}
                </Select.Item>
              {/each}
            </Select.Group>
          </Select.Content>
        </Select.Root>
      </div>
    </div>
  </div>
</header>
