<script lang="ts">
  import type { PageData } from './$types';
  import Ingredient from '$lib/components/Ingredient.svelte';

  export let data: PageData;
  const ingredients = data.ingredients;
  const steps = data.steps;

  function getImage(image_name: string) : string{
    return "http://localhost:8080/"+image_name;
  }

</script>

<main>
    <div class="whole-recipe">
      <div class="ingredients">
        {#each ingredients as ingredient}
          <Ingredient left="{ingredient.ingredient.name} " right="{+ingredient.quantity} {ingredient.unit}"/> 
        {/each}
        <div style="color=gray; font-size: 14px;">Wskazówka: Kliknij w składnik, aby oznaczyć go jako przygotowany.</div>
      </div>
      <div class="main-recipe">
        <div style="font-size:36px;">{data.name}</div>
        {data.description}<br>
        {#each steps as step}
        {step.text} <br>
        {/each}
      </div>
    </div>
    <pre>{JSON.stringify(data, null, 2)}</pre>
</main>

<style>
  .ingredients{
    margin: 1%;
    padding: 5px;
    width: 20%;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    /* background-color: red; */
  }
  .main-recipe{
    margin: 1%;
    width: 80%;
    /* background-color: blue; */
  }
  .whole-recipe{
    /* background-color: green; */
    display: flex;
    margin: 1.2%;
  }

</style>
