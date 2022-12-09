<template>
  <div id="app">
    <div id="alert" v-if="alert">{{ alert }}</div>

    <form @submit.prevent="loginWithPassword">
      <label>
        Email or username
        <input type="text" v-model="emailOrUsername" />
      </label>
      <label>
        Password
        <input type="password" v-model="password" />
      </label>
      <button type="submit">Log in</button>
    </form>

    <p>or</p>

    <button @click.prevent="loginWithSSO">
      Log in with Google
    </button>
  </div>
</template>


<style scoped>
  button,
  input {
    display: block;
    margin-bottom: 10px;
  }

  #alert {
    color: red;
    margin-bottom: 10px;
  }
</style>