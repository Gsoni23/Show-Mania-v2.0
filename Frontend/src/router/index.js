import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Dashboard from '../views/dashboard.vue'
import Venue_add from '../views/Venue_add.vue'
import Show_add from '../views/Show_add.vue'
import Show_action from '../views/Show_action.vue'
import Edit_venue from '../views/Edit_venue.vue'
import book_show from '../views/book_show.vue'
import Bookings from '../views/Bookings.vue'
import store from '../store/index.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/add-venue',
      name: 'Venue_add',
      component: Venue_add,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/add_show/:id',
      name: 'Show_add',
      component: Show_add,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/show_action/:id',
      name: 'Show_action',
      component: Show_action,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/edit_venue/:id',
      name: 'Edit_venue',
      component: Edit_venue,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/book_show/:show_id/:show_name/:show_price/:venue_id',
      name: 'book_show',
      component: book_show,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/bookings',
      name: 'bookings',
      component: Bookings,
      meta: {
        requiresAuth: true, 
      },
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.token) {
    // Redirect to login page if the route requires authentication but the token is missing
    next('/login');
  } else if (from.name === 'dashboard' && (to.name === 'login' || to.name === 'signup')) {
    // Auto logout when clicking on the backward button from the dashboard to login or signup
    store.dispatch('logout').then(() => {
      next(); 
    }).catch((error) => {
      // Handle any errors that occurred during the logout process
      console.error('Logout failed:', error);
      next(); 
    });
  } else {
    next();
  }
});


export default router
