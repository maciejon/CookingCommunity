<script>
  import '../styles/global.css';
  import Navbar from '$lib/components/Navbar.svelte';
  export const prerender = true;
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
    background-color: rgba(240, 240, 240, 0.247);
    border-top: 1px solid rgb(224,224,224); 
    text-align: center; 
    padding: 20px; 
    color: rgb(80, 80, 80); 
    font-size: 14px;
    width: 100%;
    backdrop-filter: blur(10px);
  }
</style>
