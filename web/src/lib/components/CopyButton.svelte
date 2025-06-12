<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Link2, Check } from "@lucide/svelte";

  let isCopied = $state(false);

  async function handleShare() {
    try {
      await navigator.clipboard.writeText(window.location.href);
      isCopied = true;
      setTimeout(() => {
        isCopied = false;
      }, 2000);
    } catch (err) {
      console.error("Failed to copy URL to clipboard:", err);
    }
  }
</script>

<Button
  variant="ghost"
  size="sm"
  onclick={handleShare}
  class="flex items-center gap-2 w-[100px] text-xs"
>
  {#if isCopied}
    <Check class="h-2 w-2 text-green-500" />
  {:else}
    <Link2 class="h-2 w-2" />
  {/if}
  {isCopied ? "Copied" : "Copy Link"}
</Button>
