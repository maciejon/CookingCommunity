<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

  $: recipes = data.recipes;
  $: categoryName = data.name;

  function getImage(image_name: string) : string {
    return "http://localhost:8080/" + image_name;
  }
</script>

<main>
  <h1>Przepisy w kategorii: {categoryName}</h1>
  <br>

  {#if recipes && recipes.length > 0}
    <div class="recipes-grid">
    {#each recipes as recipe (recipe.id)}
        <a href="/recipe/{recipe.slug}">
        <div class="single-recipe">
          <div class="recipe-name">
            {recipe.name}
          </div>
          
          <div class="views-counter">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
                <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
                <path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 0 1 0-1.113ZM17.25 12a5.25 5.25 0 1 1-10.5 0 5.25 5.25 0 0 1 10.5 0Z" clip-rule="evenodd" />
            </svg>
            {recipe.number_of_views}
          </div>

          <div class="recipe-time">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
              <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 6a.75.75 0 0 0-1.5 0v6c0 .414.336.75.75.75h4.5a.75.75 0 0 0 0-1.5h-3.75V6Z" clip-rule="evenodd" />
            </svg> 
            {recipe.preparation_time} min
          </div>

          <img src="{getImage(recipe.image)}" alt="{getImage(recipe.image)}" class="recipe-photo">
        </div>
        </a>
    {/each}
    </div>
  {:else}
    <p style="text-align: center; padding: 20px;">W tej kategorii nie ma jeszcze żadnych przepisów.</p>
  {/if}
  <br>
</main>

<style>
  main{
    background-color: #E3EADE;
    padding-top: 20px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }

  .recipes-grid{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    margin-bottom: 50px;  
  }
  
  @media (min-width:800px){
    .recipes-grid{
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    }
  }

  .recipe-name, .views-counter, .recipe-time{
    margin:10px;
    display: flex; 
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.6);
    position: absolute;
    border-radius: 5px;
    z-index: 10; 
    backdrop-filter: blur(10px);
  }

  .recipe-name{
    width: 50%; 
    padding: 10px; 
    bottom:0;
  }

  .views-counter, .recipe-time{
    padding-left: 10px; 
    padding-right: 10px; 
    top:0;
    gap:4px;
    align-items: center;
  }

  .recipe-time{
    right:0;
  }

  .size-6 {
    width: 20px;
    height: 20px;
  }
  
  .single-recipe{
    margin: auto;
    background-color: white;
    border-radius: 5px;
    filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, 0.4));
    width:80%;
    overflow: hidden; 
    margin-bottom: 30px;
    position: relative;
  }
  
  .single-recipe:hover .recipe-photo{
    transform: scale(1.05);
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