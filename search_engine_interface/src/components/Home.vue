<template>
  <div class="home-container">
    <img :src="logo" />
    <SearchInput ref="searchInput" @submit="onSubmit" />
    <button @click="handleSearch">Buscar</button>
  </div>
</template>

<script>
import SearchInput from "./SearchInput.vue";

export default {
  components: {
    SearchInput,
  },
  data() {
    return {
      logo: require("@/assets/logo.png"),
    };
  },
  methods: {
    handleSearch() {
      const searchInput = this.$refs["searchInput"]
      this.onSubmit(searchInput.value)
    },
    onSubmit(value) {
      if (value !== "")
        this.$router.push({
          name: "search",
          query: {
            value: value,
          },
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.home-container {
  height: 100vh;
  min-height: 500px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  > img {
    width: 350px;
    height: 180px;
    border-radius: 20px;
    margin-bottom: 50px;
  }
  > button {
    margin-top: 4rem;
    width: 120px;
    height: 40px;
    border-radius: 4px;
    background-color: #ececec78;
    cursor: pointer;
    color: #3c4043;
    font-size: 14px;
    border: 1px solid #f8f9fa;
    &:hover {
      box-shadow: 0px 0px 3px #b7b7b7;
    }
  }
}
</style>
