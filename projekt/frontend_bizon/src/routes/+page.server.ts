import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({  }) => {

  const response = await fetch(`http://127.0.0.1:8000/top5`);
  const daneZApi = await response.json();
  return daneZApi;
};