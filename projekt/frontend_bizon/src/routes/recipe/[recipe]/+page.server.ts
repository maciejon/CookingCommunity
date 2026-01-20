import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params,  request  }) => {
  const slug = params.recipe;
  const cookieHeader = request.headers.get('cookie');

  const response = await fetch(`http://127.0.0.1:8000/recipe/${slug}/`, {
    method: 'GET',
    headers: {
      'cookie': cookieHeader || '',
      'Accept': 'application/json',
    }
  });
  console.log({slug});

  const daneZApi = await response.json();
  
  return daneZApi;
};