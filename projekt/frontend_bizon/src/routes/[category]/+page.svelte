<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

  const slug = data.slug;
  const apiData = data.apiData;
</script>

<h1>Strona dla sluga: {slug}</h1>

<h2>Dane z API:</h2>
<pre>{JSON.stringify(apiData, null, 2)}</pre>