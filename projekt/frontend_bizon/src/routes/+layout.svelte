<script>
  import '../styles/global.css';
  import Navbar from '$lib/components/Navbar.svelte';
</script>


<svelte:head>
  <title>mam smaka na ptaka</title>
</svelte:head>

<div class="app-container">
  <Navbar />
  <main>
    <slot />
  </main>
  <footer>
    <p>&copy; {new Date().getFullYear()} mam smaka na ptaka. Wszelkie prawa zastrzeżone.</p>
  </footer>
</div>

<style>
  footer {
    background-color: rgb(240,240,240);
    border-top: 1px solid rgb(224,224,224); 
    text-align: center; 
    padding: 20px; 
    color: rgb(80, 80, 80); 
    font-size: 14px;
    width: 100%;
  }
</style>