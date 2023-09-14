// store/index.js
import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    token: null,
    user: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setUser(state, user) {
      state.user = user;
    },
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('setToken', token);
      commit('setUser', user);
    },
    async logout({ commit }) {
      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        await axios.post('http://127.0.0.1:5000/logout'); // Send the POST request to the logout endpoint
        commit('setToken', null);
        commit('setUser', null);
      } catch (error) {
        // Handle any errors, if needed
        console.error('Logout failed:', error);
      }
    },
    
  }
});

export default store;
