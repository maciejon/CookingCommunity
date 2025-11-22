<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

</script>

<main>
    <br>
  strona główna
  <pre>{JSON.stringify(data, null, 2)}</pre>
    <br>
</main>

<style>
 
</style>