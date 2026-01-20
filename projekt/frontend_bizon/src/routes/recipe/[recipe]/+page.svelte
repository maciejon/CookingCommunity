<script lang="ts">
  import type { PageData } from './$types';
  import Ingredient from '$lib/components/Ingredient.svelte';
  import Step from '$lib/components/Step.svelte';
  import Review from '$lib/components/Review.svelte';
  import { isAuthenticated } from '$lib/authStore.ts'
  import { invalidateAll } from '$app/navigation';

  export let data: PageData;
  const ingredients = data.ingredients;
  const steps = data.steps;
  $: reviews = data.reviews;

  function getImage(image_name: string) : string {
    return "http://localhost:8080/" + image_name;
  }
    import { createReview, updateReview } from '$lib/api.ts';

    export let recipeId: number; 
    
    let review_text = '';
    let editingReviewId: number | null = null; 
    let message = '';
    console.log(" login to:", data.requesting_user);
    $: existingReview = reviews.find(r => r.user.username === data.requesting_user);
    $: console.log(existingReview)
    let stars = 0; 
    let hoverStars = 0; 

    async function handleSubmit() {
        if (!review_text.trim() || stars === 0) {
            message = 'Proszę wpisać treść i wybrać ocenę!';
            return;
        }

        try {
          console.log(existingReview)
            if (editingReviewId) {
                await updateReview(review_text, editingReviewId, stars);
                message = 'Recenzja zaktualizowana!';
            } else {
                await createReview(review_text, data.id, stars);
                message = 'Recenzja dodana!';
                review_text = ''; 
                stars = 0; 
            }
            await invalidateAll(); 
        } catch (err) {
            message = 'Wystąpił błąd podczas zapisywania.';
            console.error(err);
        }
    }

    function startEdit(id: number, currentText: string, currentStars: number) {
        editingReviewId = id;
        review_text = currentText;
        stars = currentStars; 
    }

    function cancelEdit() {
        editingReviewId = null;
        review_text = '';
        stars = 0;
    }

</script>

<main>
    <div class="whole-recipe">
      <div class="ingredients">
        <div style="text-align:center">SKŁADNIKI</div>
        {#each ingredients as ingredient}
          <Ingredient left="{ingredient.ingredient.name} " right="{+ingredient.quantity} {ingredient.unit}"/> 
        {/each}
        <div style="color=gray; font-size: 14px;">Kliknij w składnik, aby oznaczyć go jako przygotowany.</div>
      </div>
      <div class="main-recipe">
        <div class="recipe-header">
          <div class="recipe-name-in-photo">
            {data.name}
          </div>
          <div class="recipe-description">
            {data.description}
          </div>
          <img class="recipe-photo" src="{getImage(data.image)}" alt="{data.image}"> 
        </div>
        <div class="preparation">
          <div style="text-align:center">PRZYGOTOWANIE</div>
          {#each steps as step}
            <!-- {step.text} <br> -->
            <Step content={step.text} number={step.step_number}></Step>
          {/each}
        </div>
      </div>
    </div>
    <div class="reviews">
  <div style="text-align:center">OCENY</div>

  {#if $isAuthenticated}
    <div class="review-box">
      <h3>{existingReview ? 'Edytuj swoją recenzję' : 'Dodaj nową recenzję'}</h3>
      
      <div class="star-container">
        {#each [1, 2, 3, 4, 5] as i}
          <button 
            type="button"
            class="star" 
            class:filled={i <= (hoverStars || stars)} 
            on:click={() => stars = i}
            on:mouseenter={() => hoverStars = i}
            on:mouseleave={() => hoverStars = 0}
          >
            ★
          </button>
        {/each}
        <span class="star-count">{stars}/5</span>
      </div>
      <!-- poprzednia recenzja: {existingReview.text} -->
      <form class="review-form" on:submit|preventDefault={handleSubmit}>
        <input 
            type="text" 
            bind:value={review_text}  
            placeholder="Twoja opinia..." 
            class="search-input"
        >
        <button type="submit" class="submit-button">
            {existingReview ? 'Zaktualizuj' : 'Opublikuj'}
        </button>
      </form>
    </div>
  {:else}
    <div style="margin-left: 20px;">Zaloguj się, aby dodać recenzję.</div>
  {/if}

  {#each reviews as review}
    <Review content="{review.text}" stars={review.stars} username="{review.user.username}"></Review>
  {/each}
</div>
    <!-- <pre>{JSON.stringify(data, null, 2)}</pre> -->
</main>

<style>
  *{
    font-size:20px;
  }
  main{
    background-color: #E3EADE;
    padding-bottom:10px;
  }
  .ingredients{
    margin: 1%;
    padding: 5px;
    width: 20%;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    background-color: rgb(250, 250, 250);
    filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
    position:sticky;
    top:30px;
  }
  .main-recipe{
    margin: 1%;
    width: 80%;
    /* background-color: blue; */
  }
  .whole-recipe{
    display: flex;
    margin: 1.2%;
    margin-bottom: 0;  align-items: flex-start; 
  }

  .recipe-header{
    /* background-color: green; */
    width: 100%;
    border-radius: 20px;
    overflow: hidden;
  }

  .recipe-photo{
    object-fit: cover;
    width: 100%;
    aspect-ratio: 16 / 9;
    display: block;
  }

  .recipe-name-in-photo{
    font-size: 36px;
    /* background-color: rgb(250, 250, 250);
    border-radius: 5px;
    position: absolute; */
    width: 50%; 
    margin:10px;
    display: flex; 
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.7);
    position: absolute;
    /* bottom:0; */
    border-radius: 5px;
    z-index: 10; 
    /* -webkit-backdrop-filter: blur(1px); */
    backdrop-filter: blur(1px);
  }

  .recipe-description{
    position: absolute;
    width: 40%;
    margin:10px;
    padding:5px;
    margin-top: 60px;
    display: flex; 
    justify-content: center;
    background-color: rgb(255, 255, 255, 0.4);
    position: absolute;
    border-radius: 5px;
    z-index: 10; 
    /* -webkit-backdrop-filter: blur(1px); */
    backdrop-filter: blur(10px);
  }

  .preparation{
    margin-top:20px;
    background-color: rgb(250, 250, 250);
    border-radius: 20px;
    overflow: hidden;
    filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
  }

  .reviews{
    background-color: rgb(250, 250, 250);
    border-radius: 20px;
    filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
    margin-left:35px; margin-right: 35px;
  }

  .star-container {
    display: flex;
    gap: 5px;
    align-items: center;
    margin-bottom: 10px;
    padding-left: 20px;
  }

  .star {
    background: none;
    border: none;
    font-size: 35px;
    cursor: pointer;
    color: #ccc; /* Kolor pustej gwiazdki */
    padding: 0;
    transition: transform 0.1s;
  }

  .star:hover {
    transform: scale(1.2);
  }

  /* To jest kluczowe: gwiazdki "do" klikniętej mają klasę .filled */
  .star.filled {
    color: #ffcc00; /* Kolor wypełnionej gwiazdki */
  }

  .star-count {
    margin-left: 10px;
    font-weight: bold;
    color: #666;
  }

  .review-box {
    background: #f9f9f9;
    padding: 15px;
    border-radius: 15px;
    margin: 15px;
  }
</style>
