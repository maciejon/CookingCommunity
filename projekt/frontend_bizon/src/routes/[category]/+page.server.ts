import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
  const slug = params.category;

//   console.log("tej strony slug:",{slug})
  const response = await fetch(`http://127.0.0.1:8000/category/${slug}/`);
  const daneZApi = await response.json();
  
  return {
    slug: slug,
    apiData: daneZApi
  };
};