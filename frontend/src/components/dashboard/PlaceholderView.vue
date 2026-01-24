<template>
  <div class="placeholder-container">
    <div class="icon-wrapper">
      <component :is="icon" :size="64" :stroke-width="1.5" />
    </div>
    <h2 class="title">{{ title }}</h2>
    <p class="desc">Bu modül şu an yapım aşamasındadır.</p>
    <div class="glass-decoration"></div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.placeholder-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
  position: relative;
  overflow: hidden;
  background: var(--surface-elevated);
  border-radius: 24px;
  border: 1px solid var(--border-subtle);
}

.icon-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: var(--surface-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--current-accent);
  margin-bottom: 24px;
  box-shadow: 0 0 40px var(--current-glow);
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.desc {
  color: var(--text-muted);
}

.glass-decoration {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: var(--current-accent);
  filter: blur(100px);
  opacity: 0.1;
  border-radius: 50%;
}
</style>
