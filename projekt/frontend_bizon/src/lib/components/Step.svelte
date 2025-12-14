<script>
    export let content;
    export let number;
    let isActive=true;
</script>

<main>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="step"  class:inactive={!isActive} class:active={isActive} on:click={() => isActive = !isActive} >
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
  <path fill-rule="evenodd" d="M12.53 16.28a.75.75 0 0 1-1.06 0l-7.5-7.5a.75.75 0 0 1 1.06-1.06L12 14.69l6.97-6.97a.75.75 0 1 1 1.06 1.06l-7.5 7.5Z" clip-rule="evenodd" />
</svg>
Krok {number} <br> &nbsp;&nbsp;&nbsp;&nbsp;{content}
    </div>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="step"  class:inactive={isActive} class:active={!isActive} on:click={() => isActive = !isActive} >
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
  <path fill-rule="evenodd" d="M16.28 11.47a.75.75 0 0 1 0 1.06l-7.5 7.5a.75.75 0 0 1-1.06-1.06L14.69 12 7.72 5.03a.75.75 0 0 1 1.06-1.06l7.5 7.5Z" clip-rule="evenodd" />
</svg>
    Krok {number}
    </div>
</main>

<style>
  .step{
    cursor:pointer;  
    background-color: rgb(250, 250, 250);
    padding: 4px;
    display: flex;
  }
  .step.active{
    display:block;
  }
  .step.inactive{
    display:none;
  }
  .size-6{
    width:16px;
    /* height:20px; */
  }
</style>