<script>
    import Dropdown from "./Dropdown.svelte";
</script>
<header> <!-- nagłówek strony  -->
  <img class="main_logo" src="/main_logo.png" alt = "mam smaka naptaka">
  <nav> <!--  panel nawigacyjny  -->
  <Dropdown />
  </nav>
</header>

<style>
  header{
    border-bottom: 1px solid rgb(224,224,224);
    width: 100%;
  }
  nav{
    position:fixed;
    
  }
  .main_logo{
    width: 10%;
  }
</style>