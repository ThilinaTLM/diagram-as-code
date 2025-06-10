export type Result = {
  type: "success" | "error";
  blob: Blob | null;
  error: string | null;
};

export async function getDiagramPreview(source: string): Promise<Result> {
  try {
    const response = await fetch("http://localhost:5000/diagram", {
      method: "POST",
      headers: {
        "Content-Type": "text/plain",
      },
      body: source,
    });

    if (response.ok) {
      const blob = await response.blob();
      return {
        type: "success",
        blob,
        error: null,
      };
    } else {
      if (response.status === 400) {
        const body = await response.json()
        return {
          type: "error",
          blob: null,
          error: body.detail,
        };
      }
      return {
        type: "error",
        blob: null,
        error: `Failed to generate diagram: ${response.status}`,
      };
    }
  } catch (error) {
    return {
      type: "error",
      blob: null,
      error: `Failed to generate diagram: ${
        error instanceof Error ? error.message : "Unknown error"
      }`,
    };
  }
}
