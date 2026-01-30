<template>
  <div class="home">
    <section class="hero is-large is-dark mb-6" id="custom-hero">
      <div class="hero-body has-text-centered">
        <p class="title mb-5" id="custom-text-color">Lorem ipsum</p>
        <p class="subtitle" id="custom-text-color">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.<br />
          Quisque ac mi felis. Donec nec cursus neque, vel pellentesque risus.
        </p>
      </div>
    </section>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered"><strong>Produtos</strong></h2>
      </div>
      <ProductBox
        v-for="product in latestProducts"
        v-bind:key="product.id"
        v-bind:product="product"
      />
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import ProductBox from '@/components/ProductBox.vue'

  export default {
    name: 'Home',
    data() {
      return {
        latestProducts: [],
      }
    },
    components: {
      ProductBox,
    },
    mounted() {
      this.getLatestProducts()
      document.title = 'Home | Terra Viva'
    },
    methods: {
      async getLatestProducts() {
        this.$store.commit('setIsLoading', true)
        await axios
          .get('/api/v1/latest-products/')
          .then((response) => {
            this.latestProducts = response.data
          })
          .catch((error) => {
            console.log(error)
          })
        this.$store.commit('setIsLoading', false)
      },
    },
  }
</script>

<style>
  #custom-hero {
    background-color: rgb(235, 235, 235);
  }

  #custom-text-color {
    color: #000;
  }
</style>
