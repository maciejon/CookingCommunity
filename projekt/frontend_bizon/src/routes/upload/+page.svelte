<script lang="ts">
    import { onMount } from 'svelte';
    import { getCookie } from '$lib/api';

    let availableCategories = [];
    let availableIngredients = [];
    let availableUnits = [];

    let name = "";
    let description = "";
    let preparation_time = 30;
    let selectedCategories = [];
    let steps = [{ step_number: 1, text: "" }];
    let ingredients = [{ ingredient: "", quantity: "", unit_choice: "" }];
    let imageFile = null;
    
    let loading = false;
    let message = { text: "", type: "" };

    const API_URL = "http://localhost:8000/recipe_upload/";

    onMount(async () => {
        try {
            const response = await fetch(API_URL, { credentials: 'include' });
            const data = await response.json();
            availableCategories = data.categories;
            availableIngredients = data.ingredients;
            availableUnits = data.units;
        } catch (error) {
            console.error("Błąd pobierania słowników:", error);
        }
    });

    function addStep() {
        steps = [...steps, { order: steps.length + 1, description: "" }];
    }
    function removeStep(index) {
        steps = steps.filter((_, i) => i !== index).map((s, i) => ({ ...s, order: i + 1 }));
    }

    function addIngredient() {
        ingredients = [...ingredients, { ingredient: "", amount: "", unit_choice: "" }];
    }
    function removeIngredient(index) {
        ingredients = ingredients.filter((_, i) => i !== index);
    }

    async function saveRecipe() {
        loading = true;
        
        const payload = {
            name,
            description,
            preparation_time,
            categories: selectedCategories,
            steps: steps, 
            ingredients: ingredients 
        };

        try {
            console.log(JSON.stringify(payload))
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            console.log(result);
            if (!response.ok) throw new Error(JSON.stringify(result));

            if (imageFile && result["Upload-Url"]) {
                await uploadToImageServer(result["Upload-Url"], result["Upload-Token"]);
            }

            message = { text: "Przepis dodany pomyślnie!", type: "success" };
            //resetForm();
        } catch (error) {
            message = { text: "Błąd: " + error.message, type: "error" };
        } finally {
            loading = false;
        }
    }

    async function uploadToImageServer(url, token) {
        const formData = new FormData();
        formData.append('file', imageFile);
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Upload-Token': token },
            body: formData
        });
        console.log("RES:\n:", res);
        if (!res.ok) throw new Error("Błąd przesyłania zdjęcia");
    }
</script>
<main>
<div class="recipe-form">
    <h1>Nowy Przepis</h1>



    <form on:submit|preventDefault={saveRecipe}>
        <!-- PODSTAWOWE DANE -->
        <div class="card">
            <label>Nazwa przepisu:
                <input type="text" bind:value={name} required placeholder="Np. Lasagne" />
            </label>

            <label>Opis:
                <textarea bind:value={description} placeholder="Krótki opis dania..."></textarea>
            </label>

            <label>Czas przygotowania (min):
                <input type="number" bind:value={preparation_time} min="1" />
            </label>
        </div>

        <!-- KATEGORIE (Multiselect) -->
        <div class="card">
            <h3>Kategorie</h3>
            <select multiple bind:value={selectedCategories} class="multiselect">
                {#each availableCategories as cat}
                    <option value={cat.id}>{cat.name}</option>
                {/each}
            </select>
            <small>Przytrzymaj Ctrl, aby wybrać kilka</small>
        </div>

        <!-- SKŁADNIKI -->
        <div class="card">
            <h3>Składniki</h3>
            {#each ingredients as ing, i}
                <div class="row">
                    <select bind:value={ing.ingredient} required>
                        <option value="">Wybierz składnik</option>
                        {#each availableIngredients as ai}
                            <option value={ai.id}>{ai.name}</option>
                        {/each}
                    </select>
                    <input type="number" step="0.1" bind:value={ing.quantity} placeholder="Ilość" required />
                    <select bind:value={ing.unit_choice}>
                        {#each availableUnits as u}
                            <option value={u.value}>{u.label}</option>
                        {/each}
                    </select>
                    <button type="button" on:click={() => removeIngredient(i)}>×</button>
                </div>
            {/each}
            <button type="button" class="btn-sec" on:click={addIngredient}>+ Dodaj składnik</button>
        </div>

        <!-- KROKI PRZYGOTOWANIA -->
        <div class="card">
            <h3>Kroki przygotowania</h3>
            {#each steps as step, i}
                <div class="step-row">
                    <span class="step-num">{step.step_number}.</span>
                    <textarea bind:value={step.text} placeholder="Opisz ten krok..." required></textarea>
                    <button type="button" on:click={() => removeStep(i)}>usuń</button>
                </div>
            {/each}
            <button type="button" class="btn-sec" on:click={addStep}>+ Dodaj krok</button>
        </div>

        <div class="card">
            <h3>Zdjęcie</h3>
            <input type="file" accept="image/*" on:change={e => imageFile = e.target.files[0]} />
        </div>

        <button type="submit" class="btn-main" disabled={loading}>
            {loading ? 'Trwa wysyłanie...' : 'Opublikuj przepis'}
        </button>
        {#if message.text}
            <div class="alert {message.type}">{message.text}</div>
        {/if}
    </form>
</div>
</main>

<style>
    main{
        padding: 10px;
        background-image: url('mesh-679.png');
    }
    .recipe-form { 
        max-width: 800px; 
        margin: 20px auto; 
        padding: 30px; 
        font-family: sans-serif; 
        background-color: rgba(255, 255, 255, 0.4);
        border: 2px solid rgba(184, 184, 184, 0.164);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.2));
    }

    .card { 
        background: rgba(255, 255, 255, 0.2); 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .row { 
        display: grid; 
        grid-template-columns: 2fr 1fr 1fr auto; 
        gap: 12px; 
        margin-bottom: 15px; 
    }

    .step-row { 
        display: flex; 
        gap: 10px; 
        margin-bottom: 15px; 
        align-items: flex-start; 
    }

    .step-num { 
        font-weight: bold; 
        padding-top: 10px; 
        color: #333;
    }

    textarea, 
    input[type="text"], 
    input[type="number"], 
    select { 
        width: 100%; 
        padding: 10px 12px; 
        border: 1px solid rgb(68, 68, 68); 
        border-radius: 10px; 
        background: rgba(255, 255, 255, 0.8);
        box-sizing: border-box;
        font-size: 14px;
    }

    textarea { min-height: 80px; }

    .multiselect { 
        height: 120px; 
        width: 100%; 
    }

    .btn-main { 
        width: 100%; 
        padding: 15px; 
        background-color: rgba(255, 255, 255, 0.507);
        color: #333; 
        border: 1px solid rgb(68, 68, 68); 
        border-radius: 10px; 
        font-size: 1.1em; 
        font-weight: bold;
        cursor: pointer; 
        backdrop-filter: blur(10px);
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.2));
        transition: transform 0.3s ease-in-out, background-color 0.3s;
    }

    .btn-main:hover {
        transform: scale(1.02);
        background-color: rgba(255, 255, 255, 0.7);
    }

    .btn-sec { 
        background-color: rgba(47, 53, 66, 0.8); 
        color: white; 
        border: none; 
        padding: 8px 15px; 
        border-radius: 8px; 
        cursor: pointer; 
        transition: opacity 0.3s;
    }

    .btn-sec:hover {
        opacity: 0.9;
    }

    .alert { 
        padding: 15px; 
        margin-bottom: 20px; 
        border-radius: 10px; 
        text-align: center;
        font-weight: 500;
        backdrop-filter: blur(5px);
    }

    .success { 
        background: rgba(46, 213, 115, 0.2); 
        color: #1e7a43; 
        border: 1px solid #2ed573;
    }

    .error { 
        background: rgba(214, 0, 54, 0.1); 
        color: #D60036; 
        border: 1px solid #D60036;
    }
</style>