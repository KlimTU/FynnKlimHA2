<script>
  export let size = 32;
  export let color = "#3498db";
</script>

<div
  class="spinner"
  style="width:{size}px; height:{size}px; border-top-color:{color};"
></div>

<style>
  .spinner {
    border: 3px solid #ddd;
    border-top-color: var(--color, #3498db);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-left: 14px;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
