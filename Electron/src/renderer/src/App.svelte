<script lang="ts">
  // import icons from './assets/icons.svg'
  // import Versions from './components/Versions.svelte'
  import Widget from "./components/widget.svelte";

  const amount_of_sliders = 5;
</script>

<div class="container">
  <div class="widget-container">
    {#each Array(amount_of_sliders) as _}
      <Widget />
    {/each}
  </div>
</div>

<style>
  .container {
    display: flex;
    justify-content: center;
  }

  .widget-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    width: 80%;
  }
</style>
