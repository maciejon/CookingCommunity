<script>
  import { onMount } from 'svelte';

  let apiMessage = 'Click the button to test the connection...';
  let errorMessage = '';

  async function testApiConnection() {
    errorMessage = ''; // Clear previous errors
    apiMessage = 'Fetching...';

    try {
      // The full URL to your Django endpoint
      const response = await fetch('http://127.0.0.1:8000/');
    
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      apiMessage = data.title; // Update the variable with the message from the JSON

    } catch (error) {
      // If something goes wrong, display an error message
      console.error('Failed to fetch from API:', error);
      errorMessage = `Failed to connect to the API. Is the Django server running? Error: ${error.message}`;
      apiMessage = 'Connection failed.';
    }
  }

</script>

<main>
  <h1>Svelte + Django Communication Test</h1>
  
  <button on:click={testApiConnection}>
    Test API Connection
  </button>
  
  <hr />
  
  <h2>Message from Backend:</h2>
  <p>{apiMessage}</p>

  {#if errorMessage}
    <p style="color: red;">{errorMessage}</p>
  {/if}
</main>

<style>
  main {
    font-family: sans-serif;
    text-align: center;
    padding: 2em;
  }
  button {
    padding: 10px 20px;
    font-size: 1rem;
    cursor: pointer;
  }
</style>

  
