<script setup>
</script>

<template>
 <section class="about">
      <div class="container">
        <h2>About Show-Mania</h2>
        <p>Show-Mania is an online platform that brings you a wide range of shows and events from various genres. Whether you're a fan of concerts, theater, comedy, or sports, we have something for everyone.</p>
        <p>With our easy-to-use interface, you can browse through the available shows, check out the venues, and book your tickets in just a few clicks. We strive to provide you with a seamless booking experience and ensure that you have a fantastic time at every event you attend.</p>
      </div>
    </section>
    <section class="featured-shows">
      <div class="container">
        <h2>Featured Shows</h2>
        
        <div class="show-list">
          <div class="show-card">
            <img src="../assets/lord.jpg" alt="Lord of the Rings">
            <h3>Lord of the Rings</h3>
            <p>Genre: Adventure</p>
            <router-link to="/Signup" class="btn">Book Now</router-link>

          </div>
          <div class="show-card">
            <img src="../assets/antman.jpg" alt="Ant Man">
            <h3>Ant Man</h3>
            <p>Genre: Scifi</p>
            <router-link to="/Signup" class="btn">Book Now</router-link>


          </div>
          <div class="show-card">
            <img src="../assets/bahubali.jpg" alt="Bahubali">
            <h3>Bahubali</h3>
            <p>Genre: War</p>
            <router-link to="/Signup" class="btn">Book Now</router-link>

          </div>
        </div>
      </div>
    </section>
</template>
<style>
.about {
  background-color: #f1f1f1;
  padding: 50px 0;
}

.featured-shows {
  padding: 50px 0;
}
.show-list {
  display: flex;
  justify-content: space-between;
}

.show-card {
  width: 30%;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.show-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  margin-bottom: 20px;
}

.show-card h3 {
  margin-top: 0;
}

.show-card p {
  margin-bottom: 10px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #FF5722;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
}



</style>