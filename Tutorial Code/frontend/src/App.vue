<script setup>
  import {ref} from 'vue'

  const name = ref('Rohit Kumar')
  console.log(name)
  const url = '@/assets/logo.svg'

  function changeNmae() {
    console.log("Changing name...")
    name.value = "Vue.js Developer"
  }

  const response = {
    'message': "Product fetched successfully",
    'status': 200,
    'data': {
      'id': 1,
      'name': 'Product Name',
      'description': 'Product Description',
      'price': 100.00,
    }
  }

  const isAuthenticated = ref(false)


  const role = ref('manager')
</script>

<template>
  <div>
    <h1> Welcome to my Vue App! </h1>
    <p>This is a simple Vue.js application.</p>
    <p> Hello World from {{name}}!!! </p>

    <img v-bind:src="url" alt="Vue Logo" width="100" height="100" />

    <div v-if="role === 'admin'">
        <p> Response = {{ response }}</p>
    </div>
    <div v-else-if="role === 'manager'">
       <p> You have access to the product details. </p>
    </div>
    <div v-else>
        <p> You are not authorized to view this content. </p>
    </div> 
    
    <p v-show="isAuthenticated"> You are logged in. </p>
    <p v-if="isAuthenticated"> You are logged in. </p>

    <input type="button" value = "Change Name" v-on:click = "changeNmae"/>

    <input type = "button" value = "Change IsAuthenticated" @click = "()=>{isAuthenticated = true}"/>
  </div>
</template>

<style scoped>

</style>