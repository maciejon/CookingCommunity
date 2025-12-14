<script>
    export let left;
    export let right;
    let isActive=false;
</script>

<main>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="ingredient"  class:active={isActive} on:click={() => isActive = !isActive} >
        <div class="left">{left}</div>
        <div class="right">{right}</div>
    </div>
</main>

<style>
  .ingredient{
    cursor:pointer;  
    background-color: white;
    padding: 4px;
    border: 1px solid rgb(235,235,235);
    border-radius: 3px;
    display: flex;
    margin:2px;
  }
  .ingredient.active{
    color: rgb(235,235,235);
    border-color: black;
    background-color: black;
  }
  .left{
    margin-right: auto;
    margin-left: 4px;
  }
  .right{
    margin-left: auto;
    margin-right: 4px;

  }
</style>