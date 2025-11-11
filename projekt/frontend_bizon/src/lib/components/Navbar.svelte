<script>
    import Dropdown from "./Dropdown.svelte";
</script>
<header> <!-- nagłówek strony  -->
  <div class="highest-div">
    
  <nav> <!--  panel nawigacyjny  -->
    <div class="category-buttons">
  <Dropdown
    title="Jedzenie"
    content={[
      {
        etykieta: "Śniadanie",
        children: [
          {etykieta: "Jajecznica", wartosc: "/sniadanie/jajecznica"},
          {etykieta: "Tosty", children: [
            {etykieta: "Z serem i szynką", wartosc: "/sniadanie/tosty/ser-szynka"},
            {etykieta: "Z awokado", wartosc: "/sniadanie/tosty/awokado"}
          ]},
          {etykieta: "Owsianka", wartosc: "/sniadanie/owsianka"}
        ]
      },
      {
        etykieta: "Obiad",
        children: [
          {etykieta: "Zupy", children: [
            {etykieta: "Rosół", wartosc: "/obiad/zupy/rosol"},
            {etykieta: "Pomidorowa", wartosc: "/obiad/zupy/pomidorowa"}
          ]},
          {etykieta: "Danie główne", children: [
            {etykieta: "Kotlet schabowy", wartosc: "/obiad/danie-glowne/schabowy"},
            {etykieta: "Pierogi", children: [
              {etykieta: "Ruskie", wartosc: "/obiad/danie-glowne/pierogi/ruskie"},
              {etykieta: "Z mięsem", wartosc: "/obiad/danie-glowne/pierogi/mieso"}
            ]},
            {etykieta: "Spaghetti", wartosc: "/obiad/danie-glowne/spaghetti"}
          ]}
        ]
      },
      {
        etykieta: "Kolacja",
        children: [
          {etykieta: "Kanapki", wartosc: "/kolacja/kanapki"},
          {etykieta: "Sałatka grecka", wartosc: "/kolacja/salatka-grecka"}
        ]
      },
      {
        etykieta: "Napoje",
        children: [
          {etykieta: "Gorące", children: [
            {etykieta: "Kawa", wartosc: "/napoje/gorace/kawa"},
            {etykieta: "Herbata", wartosc: "/napoje/gorace/herbata"}
          ]},
          {etykieta: "Zimne", children: [
            {etykieta: "Woda", wartosc: "/napoje/zimne/woda"},
            {etykieta: "Sok pomarańczowy", wartosc: "/napoje/zimne/sok"}
          ]}
        ]
      },
      {
        etykieta: "Desery",
        children: [
          {etykieta: "Ciasta", children: [
            {etykieta: "Sernik", wartosc: "/desery/ciasta/sernik"},
            {etykieta: "Szarlotka", wartosc: "/desery/ciasta/szarlotka"}
          ]},
          {etykieta: "Lody", wartosc: "/desery/lody"}
        ]
      }
    ]}
  />
    </div>
  </nav>
  </div>
  <div class="second-div">
    
    <img class="main_logo" src="/main_logo.png" alt = "mam smaka naptaka">

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
    width: 10%;
  }
  .highest-div{
    background-color: white;
    position:relative;
  }
  .category-buttons{
    background-color: white;
    color:black;
    display: flex;
    justify-content: center;
  }
</style>