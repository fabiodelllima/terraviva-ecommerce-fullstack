<template>
  <div class="page-success">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Obrigado!</h1>
        <p>O seu pedido será entregue em 48 horas.</p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Success',
    mounted() {
      document.title = 'Compra realizada | Terra Viva'
    },
  }
</script>
