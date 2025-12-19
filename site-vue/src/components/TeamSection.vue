<script setup>
const team = [
  {
    name: "Naledi",
    role: "Cheffe de projet",
    image: "/src/assets/Naledi.png",
    description:
      "Passionnée par la mode alternative et l’esthétisme sous toutes ses formes, je suis responsable de la conception et d’une partie du développement sur ce projet. Je crois fermement que la technologie et Internet peuvent être des leviers pour une consommation plus responsable. ",
  },
  {
    name: "Hery",
    role: "Développeur front-end",
    image: "/src/assets/Hery.png",
    description:
      "Je m’appelle Hery et je fais de l’informatique depuis 3 ans. Sur ce projet, je me suis occupé de l’API, du front-end et des requêtes vers la base de donnée, afin d’assurer une bonne cohérence globale et une bonne maintenabilité de l’application. Je suis spécialisé en développement logiciel.",
  },
  {
    name: "Emmanuel",
    role: "Développeur fullstack",
    image: "/src/assets/Manu.png",
    description:
      "Bonjour à tous, je suis un jeune développeur front-end en devenir. Malgré ma spécialisation dans le front-end, j'ai pu participer dans ce projet à la réalisation de la base de données et à sa conception, mais également au front-end.  ",
  },
  {
    name: "Zakarya",
    role: "Développeur fullstack",
    image: "/src/assets/Zak.png",
    description:
      "Je m’appelle Zakarya, je suis développeur de services métier et passionné par la mode. J’aime créer des solutions numériques et je crois que la technologie peut aider à rendre la mode plus durable.",
  },
  {
    name: "Françoise",
    role: "Développeuse front-end",
    image: "/src/assets/Solaine.png",
    description:
      "Conceptrice développeuse d’applications, je conçois et développe des solutions web fiables et maintenables. Intéressée par le back-end, l’automatisation des tests et les architectures applicatives, j’aime comprendre comment les systèmes fonctionnent en profondeur. Je crée des applications orientées qualité, performance et expérience utilisateur.",
  },
  {
    name: "Mael",
    role: "Développeur back-end",
    image: "/src/assets/Mael.png",
    description:
      "Intéressé par ce qui se passe côté serveur, j'ai participé à l'architecture back-end et l'algorithme de détection. J'aime quand c'est propre et efficace, je passe mon temps à optimiser les processus pour garantir une fluidité technique maximale.",
  },
];
</script>

<template>
  <section class="team-section">
    <h2>Notre équipe</h2>

    <article v-for="member in team" :key="member.name" class="team-member">
      <div class="avatar-wrapper">
        <img :src="member.image" :alt="member.name" class="team-avatar" />
      </div>

      <div class="team-text">
        <h3>{{ member.name }} – {{ member.role }}</h3>
        <p>{{ member.description }}</p>
      </div>
    </article>
  </section>
</template>

<style scoped>
.team-section {
  padding: 4rem 0;
  background-color: #fff5e6;
}

.team-section h2 {
  margin-left: 15%;
  margin-bottom: 3rem;
  font-style: Regular;
  color: #b70064;
  font-family: "Jersey 10";
  font-size: 48px;
  font-weight: 400;
}

.team-member {
  margin: 0 15% 3rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar-wrapper {
  width: 120px;
  height: 120px;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;
}

.team-avatar {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transform: scale(1.35);
}

.team-text h3 {
  margin-bottom: 0.5rem;

  font-family: "Jersey 10";
  font-size: 20px;
  font-weight: 400;
  color: #000;
}

.team-text p {
  max-width: 630px;

  font-family: "Inter";
  font-size: 13px;
  font-weight: 300;
  line-height: 1.5;
  text-align: justify;
}
</style>
