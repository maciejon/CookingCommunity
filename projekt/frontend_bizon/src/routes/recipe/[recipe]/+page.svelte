<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

  function getImage(image_name: string) : string{
    return "http://localhost:8080/"+image_name;
  }

</script>

<main>
    {data.name}
</main>