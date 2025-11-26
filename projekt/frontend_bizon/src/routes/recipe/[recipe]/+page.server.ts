import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
  const slug = params.recipe;

  const response = await fetch(`http://127.0.0.1:8000/recipe/${slug}/`);
  console.log({slug});
  const daneZApi = await response.json();
  
  return daneZApi;
};