<script>
    // Import komponentu Svelte
    import Dropdown from './Dropdown.svelte';

    // Definicje danych dla każdego dropdownu

    const naSkroty = {
        title: 'NA SKRÓTY',
        content: [
            { etykieta: 'Szybkie obiady', wartosc: '/szybkie-obiady' },
            { etykieta: 'Dania w 20 minut', wartosc: '/dania-20-min' },
            { 
                etykieta: 'Proste przepisy', 
                children: [
                    { etykieta: 'Sałatki', wartosc: '/proste-salatki' },
                    { etykieta: 'Zupy', wartosc: '/proste-zupy' },
                    { etykieta: 'Kanapki', wartosc: '/proste-kanapki' }
                ] 
            }
        ]
    };

    const posilki = {
        title: 'POSIŁKI',
        content: [
            { etykieta: 'Śniadania', wartosc: '/sniadania' },
            { 
                etykieta: 'Obiady', 
                children: [
                    { etykieta: 'Zupy', wartosc: '/obiady/zupy' },
                    { etykieta: 'Dania główne', wartosc: '/obiady/dania-glowne' },
                    { etykieta: 'Dodatki', wartosc: '/obiady/dodatki' }
                ]
            },
            { etykieta: 'Kolacje', wartosc: '/kolacje' },
            { etykieta: 'Przekąski', wartosc: '/przekaski' }
        ]
    };

    const skladniki = {
        title: 'SKŁADNIKI',
        content: [
            { 
                etykieta: 'Mięso', 
                children: [
                    { etykieta: 'Kurczak', wartosc: '/skladniki/kurczak' },
                    { etykieta: 'Wołowina', wartosc: '/skladniki/wolowina' },
                    { etykieta: 'Wieprzowina', wartosc: '/skladniki/wieprzowina' }
                ]
            },
            { etykieta: 'Warzywa', wartosc: '/skladniki/warzywa' },
            { etykieta: 'Owoce', wartosc: '/skladniki/owoce' },
            { etykieta: 'Nabiał', wartosc: '/skladniki/nabial' }
        ]
    };

    const naZdrowie = {
        title: 'NA ZDROWIE',
        content: [
            { etykieta: 'Fit przepisy', wartosc: '/fit' },
            { etykieta: 'Wegetariańskie', wartosc: '/wegetarianskie' },
            { etykieta: 'Wegańskie', wartosc: '/weganskie' },
            { 
                etykieta: 'Bez glutenu',
                children: [
                    { etykieta: 'Ciasta bezglutenowe', wartosc: '/bez-glutenu/ciasta' },
                    { etykieta: 'Chleby bezglutenowe', wartosc: '/bez-glutenu/chleby' }
                ]
            }
        ]
    };

    const okazje = {
        title: 'OKAZJE',
        content: [
            { etykieta: 'Święta', wartosc: '/okazje/swieta' },
            { etykieta: 'Urodziny', wartosc: '/okazje/urodziny' },
            { etykieta: 'Grill', wartosc: '/okazje/grill' },
            { etykieta: 'Impreza', wartosc: '/okazje/impreza' }
        ]
    };

    const desery = {
        title: 'DESERY',
        content: [
            { 
                etykieta: 'Ciasta',
                children: [
                    { etykieta: 'Serniki', wartosc: '/desery/ciasta/serniki' },
                    { etykieta: 'Czekoladowe', wartosc: '/desery/ciasta/czekoladowe' },
                    { etykieta: 'Owocowe', wartosc: '/desery/ciasta/owocowe' }
                ]
            },
            { etykieta: 'Lody', wartosc: '/desery/lody' },
            { etykieta: 'Ciasteczka', wartosc: '/desery/ciasteczka' }
        ]
    };
</script>
<!-- padding-left: 20px; padding-right: 20px; -->
<header> <!-- nagłówek strony  -->
  <nav> <!--  panel nawigacyjny  -->
    <div class="category-buttons">
      <div style=" padding-left: 20px; padding-right: 20px;;">
        <Dropdown title={naSkroty.title} content={naSkroty.content} />
      </div>
      <div style=" padding-left: 20px; padding-right: 20px;">
        <Dropdown title={posilki.title} content={posilki.content} />
      </div>
      <div style=" padding-left: 20px; padding-right: 20px;">
        <Dropdown title={skladniki.title} content={skladniki.content} />
      </div>
      <div style=" padding-left: 20px; padding-right: 20px;">
        <Dropdown title={naZdrowie.title} content={naZdrowie.content} />
      </div>
      <div style=" padding-left: 20px; padding-right: 20px;">
        <Dropdown title={okazje.title} content={okazje.content} />
      </div>
      <div style=" padding-left: 20px; padding-right: 20px;">
        <Dropdown title={desery.title} content={desery.content} />
      </div>

      <!-- <div style="width: 20%;">
        <Dropdown title={naSkroty.title} content={naSkroty.content}/>
      </div>
      <div style="width: 20%;">
        <Dropdown title={posilki.title} content={posilki.content} />
      </div>
      <div style="width: 20%;">
        <Dropdown title={skladniki.title} content={skladniki.content} />
      </div>
      <div style="width: 20%;">
        <Dropdown title={naZdrowie.title} content={naZdrowie.content} />
      </div>
      <div style="width: 20%;">
        <Dropdown title={okazje.title} content={okazje.content} />
      </div>
      <div style="width: 20%;">
        <Dropdown title={desery.title} content={desery.content} />
      </div> -->


      <!-- <Dropdown title={naSkroty.title} content={naSkroty.content} />
      <Dropdown title={posilki.title} content={posilki.content} />
      <Dropdown title={skladniki.title} content={skladniki.content} />
      <Dropdown title={naZdrowie.title} content={naZdrowie.content} />
      <Dropdown title={okazje.title} content={okazje.content} />
      <Dropdown title={desery.title} content={desery.content} /> -->
    </div>
  </nav>

  <div class="second-div">
    <div class="main_logo">
      <a href="http://localhost:5173" >
        <img style="width: 100%" src="/main_logo.png" alt="mam smaka naptaka">
      </a>
    </div>

    <div style="width: 50%; margin: auto; ">
      <form class="search-bar" method="POST">
                <input type="text" name="query" placeholder="Wyszukaj..." class="search-input">
                <button type="submit" class="search-button">
                    <img src="/search_icon.png" alt="Szukaj" class="search-icon">
                </button>
            </form>
    </div>

  </div>
</header>

<style>
  header{
    border-bottom: 1px solid rgb(224,224,224);
    width: 100%;
  }
  nav{
    position:relative;
    
  }
  .main_logo{
    width: 11%;
    padding: 5px; 
  }
  .category-buttons{
    background-color: black;
    color:white;
    display: flex;
    justify-content: center;
    padding-left: 20%;
    padding-right: 20%;
  }
  .second-div{
    display: flex;
  }
  .search-bar {
    display: flex;
    align-items: center;
    background-color: #e0e0e0; 
    border-radius: 5px;
    padding: 5px;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-input {
    flex-grow: 1;
    border: none;
    outline: none;
    background: transparent;
    padding: 5px 10px;
    font-size: 16px;
}

.search-button {
    background-color: #D60036;
    border: none;
    padding: 5px;
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
}

.search-icon {
    width: 16px;
    height: 16px;
    object-fit: contain;
}

.search-button:hover {
    transform: scale(1.1);
}
</style>