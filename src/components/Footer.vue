<script setup>

</script>
<template>
  <footer class="footer">
    <div>
      <small>© 2025 Starfield — Made with ❤️ using OpenCV</small>
    </div>
    <div class="footer-links">
      <a href="https://github.com/mds7677/Starfield" target="_blank">GitHub</a>
      <a href="/authors">Authors</a>
      <a href="/about">About</a>
    </div>
    <router-view/>
  </footer>
</template>
<style>
.footer {
background-color: #0a0f1c;
color: #c9d1d9;
font-family: 'Orbitron', sans-serif;
font-size: 18px;
padding: 20px 30px;
border-top: 1px solid #131924;
display: flex;
flex-direction: column;
align-items: center;
text-align: center;
margin-top: 160px;
}

.footer a {
color: #58a6ff;
text-decoration: none;
margin: 0 8px;
transition: color 0.2s ease;
}

.footer a:hover {
color: #84c5ff;
}

.footer .footer-links {
margin-top: 8px;
display: flex;
gap: 16px;
flex-wrap: wrap;
justify-content: center;
}

.footer small {
opacity: 0.7;
}
</style>