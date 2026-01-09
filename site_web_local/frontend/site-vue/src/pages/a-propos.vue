<template>
  <div class="a-propos-page">
    <div class="container">
      <h1 class="title">À propos de nous</h1>
      <div class="content">
        <div class="text-section">
          <h2 class="section-title">Notre Mission</h2>
          <p>Greenstyle est une plateforme dédiée à la mode durable et responsable.</p>
          <p>Notre mission est d'aider les consommateurs à faire des choix éclairés en matière de mode.</p>
        </div>
        <div class="image-section">
          <img src="/src/assets/heel-plant.png" alt="Greenstyle" class="about-image" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.a-propos-page {
  min-height: calc(100vh - 85px);
  background: var(--page-bg, #DBC9AF);
  padding: 40px 0;
}

.container {
  max-width: 100%;
  margin: 0 15%;
}

.title {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 36px;
  color: var(--green-dark, #017740);
  margin-bottom: 32px;
  text-align: center;
}

.content {
  background: var(--panel-bg, #F4E8D7);
  padding: 32px;
  border-radius: 8px;
  border: 3px solid var(--green-dark, #017740);
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 32px;
}

.text-section {
  flex: 1;
}

.section-title {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 28px;
  color: var(--green-dark, #017740);
  margin-bottom: 20px;
}

.content p {
  font-size: 18px;
  line-height: 1.6;
  color: var(--green-dark, #017740);
  margin-bottom: 16px;
}

.image-section {
  flex-shrink: 0;
}

.about-image {
  max-width: 300px;
  height: auto;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .container {
    margin: 0 5%;
  }
  
  .content {
    flex-direction: column;
    text-align: center;
  }
  
  .about-image {
    max-width: 200px;
  }
}
</style>


