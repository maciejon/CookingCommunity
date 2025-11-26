<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

  $: recipes = data.recipes;
  $: categoryName = data.name;

  function getImage(image_name: string) : string{
    return "http://localhost:8080/"+image_name;
  }

</script>

<h1>Przepisy w kategorii: {categoryName} <br></h1>

{#if recipes && recipes.length > 0}
    <div class="recipes-grid">
    {#each recipes as recipe (recipe.id)}
        <a href="recipe/{recipe.slug}">
        <div class="single-recipe">
          <div class="recipe-name">
          {recipe.name}
          </div>
          <img src="{getImage(recipe.image)}" alt="localhost:8080/{recipe.image}" class="recipe-photo">
        </div>
        </a>
    {/each}
    </div>
{:else}
  <p>W tej kategorii nie ma jeszcze żadnych przepisów.</p>
{/if}
<!-- <pre>{JSON.stringify(recipes, null, 2)}</pre> -->

<style>
  .recipes-grid{
    display: grid;
    grid-template-columns: auto auto auto;
    margin-bottom: 50px;
  }
  .recipe-name{
    width: 100%; 
    padding: 10px; 
    display: flex; 
    justify-content: center;
    background-color: white;
  }
  .single-recipe{
    margin: auto;
    background-color: white;
    border: 1px solid black;
    filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, 0.4));
    width:80%;
    overflow: hidden; 
  }
  .single-recipe:hover .recipe-photo{
    transform: scale(1.05);
    /* zoom: 1.1; */
  }
  .recipe-photo{
    object-fit: cover;
    width: 100%;
    aspect-ratio: 16 / 9;
    transition: transform 0.3s ease-in-out;
    display: block;
  }
  a{
    color: inherit;
    text-decoration: none;
  }
</style>