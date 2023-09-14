import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// Set up Axios interceptors
axios.interceptors.response.use(
    (response) => response,
    (error) => {
      // If the response status is 401, redirect to the login page
      if (error.response && error.response.status === 401) {
        router.push('/login'); // Change '/login' to the actual login route path
      }
      return Promise.reject(error);
    }
);

const app = createApp(App)

app.use(router)
app.use(store)



app.mount('#app')
