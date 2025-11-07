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

</style>