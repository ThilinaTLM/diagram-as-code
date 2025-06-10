<script lang="ts">
  import { onMount } from "svelte";

  interface Props {
    src: string;
    alt?: string;
    class?: string;
  }

  let { src, alt = "Diagram", class: className = "" }: Props = $props();

  let containerRef: HTMLDivElement;
  let imageRef: HTMLImageElement;

  let scale = $state(1);
  let translateX = $state(0);
  let translateY = $state(0);
  let isDragging = $state(false);
  let dragStart = $state({ x: 0, y: 0 });
  let lastTranslate = $state({ x: 0, y: 0 });

  const MIN_SCALE = 0.1;
  const MAX_SCALE = 5;
  const ZOOM_STEP = 0.1;

  function handleWheel(event: WheelEvent) {
    event.preventDefault();

    const rect = containerRef.getBoundingClientRect();
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    // Mouse position relative to container
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    // Calculate zoom
    const delta = event.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP;
    const newScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, scale + delta));

    if (newScale !== scale) {
      // Zoom towards mouse position
      const scaleRatio = newScale / scale;

      translateX = mouseX - (mouseX - translateX) * scaleRatio;
      translateY = mouseY - (mouseY - translateY) * scaleRatio;

      scale = newScale;
    }
  }

  function handleMouseDown(event: MouseEvent) {
    if (event.button === 0) {
      // Left mouse button
      isDragging = true;
      dragStart = { x: event.clientX, y: event.clientY };
      lastTranslate = { x: translateX, y: translateY };

      // Prevent image dragging
      event.preventDefault();
    }
  }

  function handleMouseMove(event: MouseEvent) {
    if (isDragging) {
      const deltaX = event.clientX - dragStart.x;
      const deltaY = event.clientY - dragStart.y;

      translateX = lastTranslate.x + deltaX;
      translateY = lastTranslate.y + deltaY;
    }
  }

  function handleMouseUp() {
    isDragging = false;
  }

  function handleDoubleClick() {
    // Reset to fit container
    resetView();
  }

  function resetView() {
    scale = 1;
    translateX = 0;
    translateY = 0;
  }

  function zoomIn() {
    const newScale = Math.min(MAX_SCALE, scale + ZOOM_STEP * 2);
    if (newScale !== scale) {
      scale = newScale;
    }
  }

  function zoomOut() {
    const newScale = Math.max(MIN_SCALE, scale - ZOOM_STEP * 2);
    if (newScale !== scale) {
      scale = newScale;
    }
  }

  function fitToContainer() {
    if (!imageRef || !containerRef) return;

    const containerRect = containerRef.getBoundingClientRect();
    const imageRect = imageRef.getBoundingClientRect();

    const scaleX = (containerRect.width * 0.9) / imageRef.naturalWidth;
    const scaleY = (containerRect.height * 0.9) / imageRef.naturalHeight;

    scale = Math.min(scaleX, scaleY, 1);
    translateX = 0;
    translateY = 0;
  }

  onMount(() => {
    // Add global mouse event listeners
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  });

  // Reset view when src changes
  let previousSrc = $state(src);
  $effect(() => {
    if (src !== previousSrc) {
      previousSrc = src;
      resetView();
    }
  });
</script>

<div
  bind:this={containerRef}
  class="relative w-full h-full overflow-hidden bg-background {className}"
  onwheel={handleWheel}
  onmousedown={handleMouseDown}
  ondblclick={handleDoubleClick}
  style="cursor: {isDragging ? 'grabbing' : 'grab'}"
  role="presentation"
  aria-label="Interactive diagram viewer - scroll to zoom, drag to pan, double-click to reset"
>
  <!-- Zoom Controls -->
  <div
    class="absolute top-4 right-4 z-10 flex flex-col gap-2 bg-background/80 backdrop-blur-sm rounded-lg p-2 border shadow-sm"
  >
    <button
      onclick={zoomIn}
      class="w-8 h-8 flex items-center justify-center rounded hover:bg-muted transition-colors"
      title="Zoom In"
      aria-label="Zoom In"
    >
      <svg
        class="w-4 h-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 6v6m0 0v6m0-6h6m-6 0H6"
        />
      </svg>
    </button>

    <button
      onclick={zoomOut}
      class="w-8 h-8 flex items-center justify-center rounded hover:bg-muted transition-colors"
      title="Zoom Out"
      aria-label="Zoom Out"
    >
      <svg
        class="w-4 h-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M18 12H6"
        />
      </svg>
    </button>

    <button
      onclick={fitToContainer}
      class="w-8 h-8 flex items-center justify-center rounded hover:bg-muted transition-colors"
      title="Fit to Screen"
      aria-label="Fit to Screen"
    >
      <svg
        class="w-4 h-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
        />
      </svg>
    </button>

    <button
      onclick={resetView}
      class="w-8 h-8 flex items-center justify-center rounded hover:bg-muted transition-colors"
      title="Reset View"
      aria-label="Reset View"
    >
      <svg
        class="w-4 h-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
        />
      </svg>
    </button>
  </div>

  <!-- Scale indicator -->
  <div
    class="absolute bottom-4 left-4 z-10 bg-background/80 backdrop-blur-sm rounded px-2 py-1 text-xs border shadow-sm"
  >
    {Math.round(scale * 100)}%
  </div>

  <!-- Image -->
  <div
    class="absolute inset-0 flex items-center justify-center"
    style="transform: translate({translateX}px, {translateY}px) scale({scale}); transform-origin: center;"
  >
    <img
      bind:this={imageRef}
      {src}
      {alt}
      class="max-w-none select-none"
      draggable="false"
      onload={fitToContainer}
    />
  </div>

  <!-- Instructions overlay (shown when no interaction) -->
  {#if !isDragging && scale === 1 && translateX === 0 && translateY === 0}
    <div
      class="absolute bottom-4 right-4 z-10 bg-background/80 backdrop-blur-sm rounded px-3 py-2 text-xs text-muted-foreground border shadow-sm max-w-48"
    >
      <div class="space-y-1">
        <div>• Scroll to zoom</div>
        <div>• Drag to pan</div>
        <div>• Double-click to reset</div>
      </div>
    </div>
  {/if}
</div>
