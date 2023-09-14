<template>
    <div>
        <form @submit.prevent="updateShow" class="add-show-form">
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  
          <h2>Actions</h2>
            <div class="form-group">
              <label for="show_name">Show Name:</label>
              <input type="text" id="show_name" v-model="show_name" required>
            </div>
            <div class="form-group">
              <label for="rating">Rating:</label>
              <input type="number" id="rating" v-model="rating" required>
            </div>
            <div class="form-group">
              <label for="start_time">Start Time:</label>
              <input type="time" id="start_time" v-model="start_time" required>
            </div>
            <div class="form-group">
              <label for="end_time">End Time:</label>
              <input type="time" id="end_time" v-model="end_time" required>
            </div>
            <div class="form-group">
              <label for="tags">Tags:</label>
              <input type="text" id="tags" v-model="tags" required>
            </div>
            <div class="form-group">
              <label for="price">Ticket Price:</label>
              <input type="number" id="price" v-model="price" required>
            </div>
          <button type="submit" class="btn-addshow">Update</button>
          <button @click="deleteShow" class="btn btn-delete">Delete</button>

        </form>

      </div>
</template>
  
<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';
    import store from '../store';
  
    const route = useRouter();
    const show_id = route.currentRoute.value.params.id;
  
    
    const show_name = ref('');
    const rating = ref('');
    const start_time = ref('');
    const end_time = ref('');
    const tags = ref('');
    const price = ref('');

    
    const errorMessage = ref('');

    // Fetch the show details from the backend API when the component is mounted
    onMounted(async () => {
      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get('http://127.0.0.1:5000/show', {params : {show_id:show_id}});
        show_name.value = response.data.show_name;
        rating.value = response.data.rating;
        start_time.value = response.data.start_time;
        end_time.value = response.data.end_time;
        tags.value = response.data.tags;
        price.value = response.data.price;

        // console.log(response.data);

      } catch (error) {
        console.error(error);
        
      }
    });
  
    async function updateShow() {
      try {

        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.patch('http://127.0.0.1:5000/show', {
          show_name: show_name.value,
          rating: rating.value,
          start_time: start_time.value.substring(0,5),
          end_time: end_time.value.substring(0,5),
          tags: tags.value,
          price: price.value,
        }, {
          params: {
            show_id: show_id
          }
        });
  
  
        // Handle success and show feedback to the user
        console.log(response.data.message);
        route.push('/dashboard');
      } catch (error) {
        errorMessage.value = 'An error occurred during show updation. Please try again later.';
        console.error(error);
      }
    }
  
    async function deleteShow() {
        // Prevent the form submission
        event.preventDefault(); 

      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.delete(`http://127.0.0.1:5000/show`, {
          params: {
            show_id: show_id
          }
        });
  
        // Handle success and show feedback to the user
        console.log(response.data.message);
        route.push('/dashboard');
      } catch (error) {
        // Handle error and show feedback to the user (e.g., toast message)
        errorMessage.value = 'An error occurred during show deletion. Please try again later.';
        console.error(error);
      }
    }
</script>
  
<style>
.error-message {
    color: #dc3545;
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    background-color: #f8d7da;
    border-radius: 4px;
    text-align: center;
  }
  
  .add-show-form {
    max-width: 4000px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f1f1f1;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-group label {
    display: block;
    font-weight: bold;
  }
  .form-group input {
    width: 50%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .btn-addshow {
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 6px;
    cursor: pointer;
    margin: 0 5px;
    border: none;
    color: #fff;
    background-color: #FF5722;
  }
  
  .btn-addshow:hover {
      filter: brightness(85%);
    }

    .btn-delete {
        background-color: #dc3545;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 6px;
        cursor: pointer;
        margin: 0 5px;
        border: none;
        color: #fff;
    }

    .btn-delete:hover {
        filter: brightness(85%);
    }
</style>
  