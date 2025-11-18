<script>
    let daneZBackendu = 'Oczekiwanie na dane...';

  // Funkcja, która będzie wysyłać zapytanie GET
  async function pobierzDane(zrodlo) {
    // Ustawiamy podstawowy adres URL naszego API
    const baseUrl = 'http://127.0.0.1:8000';
    
    // Tworzymy obiekt URLSearchParams, aby bezpiecznie dodać parametry
    const params = new URLSearchParams({
      zrodlo: zrodlo  // np. zrodlo=przycisk1
    });

    // Pełny adres URL z parametrem zapytania
    const url = `${baseUrl}?${params.toString()}`;

    console.log(`Wysyłam zapytanie na adres: ${url}`);

    try {
      const odpowiedz = await fetch(url);
      
      if (!odpowiedz.ok) {
        throw new Error(`Błąd HTTP! Status: ${odpowiedz.status}`);
      }
      
      const dane = await odpowiedz.json();
      daneZBackendu = JSON.stringify(dane, null, 2); // Formatujemy JSON dla czytelności

    } catch (error) {
      console.error('Nie udało się pobrać danych:', error);
      daneZBackendu = 'Wystąpił błąd podczas ładowania danych.';
    }
  }
</script>

<main>
    <br>
  strona główna
    <br>
</main>

<style>
 
</style>