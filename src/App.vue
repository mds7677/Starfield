<template>
    <MyButton/>

  <div style="display: flex;flex-direction: column">
    <MyStars/>
    <MyInput/>
  </div>
  <div class = "text">
  <MyText
  v-for="post in posts"
  :key ="post.id"
  :title = "post.title"
  :head ="post.head"
  ></MyText>
  </div>




</template>

<script setup>
import MyStars from './components/Stars.vue';
import MyInput from './components/Input.vue';
import MyText from './components/Text.vue';
import MyButton from './components/MenuButton.vue';
import {ref} from "vue";
const posts = ref([
  { id: 1, head :"Gemini",title: 'Близнецы — зодиакальное созвездие, символизирует братьев Кастора и Поллукса. Наиболее яркие звёзды — Кастор и Поллукс.' },
  { id: 2, head :"Andromeda",title: 'Андромеда — расположено в северном полушарии, известно галактикой Андромеды — ближайшей крупной к Млечному Пути.' },
  { id: 3, head :"Orion",title: 'Орион — одно из самых узнаваемых созвездий, включает пояс Ориона. Содержит яркую звезду Бетельгейзе и туманность Ориона.' },
  { id: 4, head:"Ursa Major",title:"Большая Медведица — одно из самых известных созвездий, содержит астеризм Большая Медведица (Ковш)."},
  { id: 5, head:"Ursa Minor",title:"Малая Медведица — включает Полярную звезду, указывающую на север, также известна своим 'маленьким ковшом'."},
  { id: 6, head:"Aquila",title:"Орел — включает яркую звезду Альтаир, часть Летнего треугольника. Названо в честь орла Зевса."},
  { id: 7, head:"Cancer",title:"Рак — зодиакальное созвездие, менее яркое, но известно скоплением Улей (Пчелиный рой)."},
  { id: 8, head:"Phoenix",title:"Феникс — южное созвездие, названо в честь мифической птицы, возрождающейся из пепла. Открыто в 16 веке."},
  { id: 9, head:"Aquarius",title:"Водолей — зодиакальное созвездие, символизирует водоносца. Входит в зодиак и ассоциируется с потоком воды."},
  { id:10, head: "Leo", title: "Лев — зодиакальное созвездие, символизирует льва из мифов. Содержит яркую звезду Регул и хорошо видно весной."}
])
</script>

<style>
body{
  display: flex;
  flex-direction: column;
  background-color: black;
}
.text{
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  height: 500px;
  justify-content: space-between;
  align-items: center;
}

</style>
