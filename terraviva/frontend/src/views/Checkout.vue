<template>
  <div class="page-checkout">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Finalizar compra</h1>
      </div>
      <div class="column is-12 box">
        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Produto</th>
              <th>Preço</th>
              <th>Quantidade</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.items" v-bind:key="item.product.id">
              <td>{{ item.product.name }}</td>
              <td>${{ item.product.price }}</td>
              <td>{{ item.quantity }}</td>
              <td>${{ getItemTotal(item).toFixed(2) }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2">Total</td>
              <td>{{ cartTotalLength }}</td>
              <td>${{ cartTotalPrice.toFixed(2) }}</td>
            </tr>
          </tfoot>
        </table>
      </div>
      <div class="column is-12 box">
        <h2 class="subtitle">Detalhes da compra</h2>
        <p class="has-text-grey mb-4">* Todos os campos precisam ser preenchidos.</p>
        <div class="columns is-multiline">
          <div class="column is-6">
            <div class="field">
              <label>Nome*</label>
              <div class="control">
                <input type="text" class="input" v-model="first_name" />
              </div>
            </div>
            <div class="field">
              <label>Sobrenome*</label>
              <div class="control">
                <input type="text" class="input" v-model="last_name" />
              </div>
            </div>
            <div class="field">
              <label>E-mail*</label>
              <div class="control">
                <input type="email" class="input" v-model="email" />
              </div>
            </div>
            <div class="field">
              <label>Telefone*</label>
              <div class="control">
                <input type="text" class="input" v-model="phone" />
              </div>
            </div>
          </div>
          <div class="column is-6">
            <div class="field">
              <label>Endereço*</label>
              <div class="control">
                <input type="text" class="input" v-model="address" />
              </div>
            </div>
            <div class="field">
              <label>CEP*</label>
              <div class="control">
                <input type="text" class="input" v-model="zipcode" />
              </div>
            </div>
            <div class="field">
              <label>Bairro*</label>
              <div class="control">
                <input type="text" class="input" v-model="place" />
              </div>
            </div>
          </div>
        </div>
        <div class="notification is-danger mt-4" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>
        <hr />
        <div id="card-element" class="mb-5"></div>
        <template v-if="cartTotalLength">
          <hr />
          <button class="button is-dark" @click="submitForm">Pagar com Stripe</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'Checkout',
    data() {
      return {
        cart: {
          items: [],
        },
        stripe: {},
        card: {},
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address: '',
        zipcode: '',
        place: '',
        errors: [],
      }
    },
    mounted() {
      document.title = 'Finalizar compra | Terra Viva'
      this.cart = this.$store.state.cart
      if (this.cartTotalLength > 0) {
        this.stripe = Stripe(
          'pk_test_51H1HiuKBJV2qfWbD2gQe6aqanfw6Eyul5PO2KeOuSRlUMuaV4TxEtaQyzr9DbLITSZweL7XjK3p74swcGYrE2qEX00Hz7GmhMI'
        )
        const elements = this.stripe.elements()
        this.card = elements.create('card', { hidePostalCode: true })
        this.card.mount('#card-element')
      }
    },
    methods: {
      getItemTotal(item) {
        return item.quantity * item.product.price
      },
      submitForm() {
        this.errors = []
        if (this.first_name === '') {
          this.errors.push('O Nome precisa ser preenchido!')
        }
        if (this.last_name === '') {
          this.errors.push('O Sobrenome precisa ser preenchido!')
        }
        if (this.email === '') {
          this.errors.push('O E-mail precisa ser preenchido!')
        }
        if (this.phone === '') {
          this.errors.push('O Telefone precisa ser preenchido!')
        }
        if (this.address === '') {
          this.errors.push('O Endereço precisa ser preenchido!')
        }
        if (this.zipcode === '') {
          this.errors.push('O CEP precisa ser preenchido!')
        }
        if (this.place === '') {
          this.errors.push('O Bairro precisa ser preenchido!')
        }
        if (!this.errors.length) {
          this.$store.commit('setIsLoading', true)
          this.stripe.createToken(this.card).then((result) => {
            if (result.error) {
              this.$store.commit('setIsLoading', false)
              this.errors.push('Algo deu errado. Tente mais uma vez.')
              console.log(result.error.message)
            } else {
              this.stripeTokenHandler(result.token)
            }
          })
        }
      },
      async stripeTokenHandler(token) {
        const items = []
        for (let i = 0; i < this.cart.items.length; i++) {
          const item = this.cart.items[i]
          const obj = {
            product: item.product.id,
            quantity: item.quantity,
            price: item.product.price * item.quantity,
          }
          items.push(obj)
        }
        const data = {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          address: this.address,
          zipcode: this.zipcode,
          place: this.place,
          phone: this.phone,
          items: items,
          stripe_token: token.id,
        }
        await axios
          .post('/api/v1/checkout/', data)
          .then((_response) => {
            this.$store.commit('clearCart')
            this.$router.push('/cart/success')
          })
          .catch((error) => {
            this.errors.push('Algo deu errado. Tente mais uma vez.')
            console.log(error)
          })
        this.$store.commit('setIsLoading', false)
      },
    },
    computed: {
      cartTotalPrice() {
        return this.cart.items.reduce((acc, curVal) => {
          return (acc += curVal.product.price * curVal.quantity)
        }, 0)
      },
      cartTotalLength() {
        return this.cart.items.reduce((acc, curVal) => {
          return (acc += curVal.quantity)
        }, 0)
      },
    },
  }
</script>
