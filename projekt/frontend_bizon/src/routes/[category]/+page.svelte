<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

  const recipes = data.recipes;
  const categoryName = data.name;

</script>

<h1>Przepisy w kategorii: {categoryName}</h1>

{#if recipes && recipes.length > 0}
  <ul>
    {#each recipes as recipe (recipe.id)}
      <li>
        <h3>{recipe.name}</h3>
        <p>Czas przygotowania: {recipe.preparation_time} minut</p>
      </li>
    {/each}
  </ul>
{:else}
  <p>W tej kategorii nie ma jeszcze żadnych przepisów.</p>
{/if}