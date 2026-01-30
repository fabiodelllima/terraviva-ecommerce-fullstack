<template>
  <div id="wrapper">
    <nav class="navbar is-transparent">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item" id="custom-logo">
          &nbsp;&nbsp;&nbsp;terra<strong>viva</strong>
        </router-link>
        <a
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                  <input type="text" class="input" placeholder="Pesquisar..." name="query" />
                </div>
                <div class="control">
                  <button class="button is-success">
                    <span class="icon">
                      <i class="fas fa-search"></i>
                    </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
        <div class="navbar-end">
          <router-link to="/legumes" class="navbar-item" id="custom-hover"> Legumes </router-link>
          <router-link to="/frutas" class="navbar-item" id="custom-hover"> Frutas </router-link>
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/my-account" class="button is-success is-outlined">
                  Minha conta
                </router-link>
              </template>
              <template v-else>
                <router-link to="/log-in" class="button is-success is-outlined">
                  Login
                </router-link>
              </template>
              <router-link to="/cart" class="button is-success" id="custom-cart">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>Carrinho ({{ cartTotalLength }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div
      class="is-loading-bar has-text-centered"
      v-bind:class="{ 'is-loading': $store.state.isLoading }"
    >
      <div class="lds-dual-ring"></div>
    </div>
    <section class="section">
      <router-view />
    </section>
    <footer class="footer" id="custom-footer">
      <div class="custom-footer-wrapper">
        <div class="custom-footer-box a">
          <div>
            <p id="custom-logo-footer">terra<strong id="custom-strong-footer">viva</strong></p>
          </div>
          <div>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis scelerisque tempus eros,
              at auctor mauris porta id. Donec venenatis eros in sapien tempus, sed pulvinar sapien
              egestas. Integer eu euismod est.
            </p>
          </div>
        </div>
        <div class="custom-footer-box b">
          <div>
            <p id="custom-logo">categorias</p>
            <ul>
              <li>&nbsp;Link #1</li>
              <li>&nbsp;Link #2</li>
              <li>&nbsp;Link #3</li>
              <li>&nbsp;Link #4</li>
              <li>&nbsp;Link #5</li>
            </ul>
          </div>
        </div>
        <div class="custom-footer-box c">
          <div>
            <p id="custom-logo">links</p>
            <ul>
              <li>&nbsp;Link #1</li>
              <li>&nbsp;Link #2</li>
              <li>&nbsp;Link #3</li>
              <li>&nbsp;Link #4</li>
              <li>&nbsp;Link #5</li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    data() {
      return {
        showMobileMenu: false,
        cart: {
          items: [],
        },
      }
    },
    beforeCreate() {
      this.$store.commit('initializeStore')
      const token = this.$store.state.token
      if (token) {
        axios.defaults.headers.common['Authorization'] = 'Token ' + token
      } else {
        axios.defaults.headers.common['Authorization'] = ''
      }
    },
    mounted() {
      this.cart = this.$store.state.cart
    },
    computed: {
      cartTotalLength() {
        let totalLength = 0
        for (let i = 0; i < this.cart.items.length; i++) {
          totalLength += this.cart.items[i].quantity
        }
        return totalLength
      },
    },
  }
</script>

<style lang="scss">
  @import '../node_modules/bulma';
  @import url('https://fonts.googleapis.com/css2?family=Montserrat+Alternates:wght@300;800&display=swap');

  strong {
    font-weight: bold;
  }

  .lds-dual-ring {
    display: inline-block;
    width: 80px;
    height: 80px;
  }

  .lds-dual-ring:after {
    content: ' ';
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #ccc;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
  }

  @keyframes lds-dual-ring {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(360deg);
    }
  }

  .is-loading-bar {
    height: 0;
    overflow: hidden;
    -webkit-transition: all 0.3s;
    transition: all 0.3s;

    &.is-loading {
      height: 80px;
    }
  }

  #custom-logo {
    white-space: nowrap;
    gap: 0;
    font-family: 'Montserrat Alternates', sans-serif;
    color: hsl(141, 53%, 53%);
    font-size: 2.5em;
    display: inline;
    gap: 0;
  }

  /* NAVBAR HOVER LINKS */
  #custom-hover:hover {
    color: hsl(141, 53%, 53%);
  }

  /* NAVBAR FONT SIZE */
  button {
    font-size: 1.2em;
  }

  .navbar-item {
    font-size: 1.2em;
  }

  /* CART BUTTON MARGIN */
  #custom-cart {
    margin-right: 35px;
  }

  /* HTML HEIGHT TO FIX FOOTER */
  html {
    height: 100%;
  }

  body {
    min-height: 100%;
    padding: 0;
    margin: 0;
    position: relative;
  }

  body::after {
    content: '';
    display: block;
    height: 240px;
  }

  /* CUSTOM FOOTER */
  #custom-footer {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 240px;
    padding: 0;
    background-color: #000;
  }

  .custom-footer-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    background-color: #000;
    padding: 0;
    margin: 0;
  }

  .custom-footer-box {
    background-color: #000;
    color: #fff;
    border-radius: 5px;
    padding: 10px;
    margin: 10px;
    font-size: 1em;
  }

  @media (min-width: 801px) {
    .custom-footer-box:first-child {
      max-width: 680px;
    }
  }

  @media (max-width: 900px) {
    .custom-footer-box {
      flex: 100%;
    }
  }

  #custom-logo-footer {
    font-family: 'Montserrat Alternates', sans-serif;
    color: hsl(141, 53%, 53%);
    font-size: 2.5em;
  }

  #custom-strong-footer {
    color: hsl(141, 53%, 53%);
  }

  /* CUSTOM LINKS */
  #custom-link {
    box-shadow: inset 0 -7px 0 #a0ffc1;
    color: #000;
  }

  #custom-link:hover {
    box-shadow: inset 0 -5px 0 #fff;
    color: #48c774;
  }

  /* CUSTOM ROUTER-LINK */
  a.router-link-active {
    color: #48c774;
  }

  a.router-link-exact-active {
    color: #48c774;
  }

  .router-link-active a {
    color: #48c774;
  }

  .router-link-exact-active a {
    color: #48c774;
  }
  /* Bulma 1.0 fixes */
  .button.is-success {
    color: #fff !important;
  }
  .button.is-success .icon {
    color: #fff !important;
  }
  .button.is-success:hover {
    color: #fff !important;
  }
  .button.is-success.is-outlined {
    color: #48c774 !important;
    background-color: transparent !important;
  }
  .button.is-success.is-outlined:hover {
    color: #fff !important;
    background-color: #48c774 !important;
  }
  .navbar-item:hover,
  .navbar-item.router-link-active,
  .navbar-item.router-link-exact-active {
    background-color: transparent !important;
  }
</style>
