import type { PageServerLoad } from './$types';
  import { apiFetch } from '$lib/api.ts';

export const load: PageServerLoad = async ({  }) => {

  const response = await fetch(`http://127.0.0.1:8000/top5`);
  const daneZApi = await response.json();
  return daneZApi;
};

