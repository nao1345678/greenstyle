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
      "Passionné par le côté serveur, j’ai travaillé sur l’architecture back-end et les algorithmes de détection.",
  },
];
</script>

<template>
  <section class="team-section">
    <h2>Notre équipe</h2>

    <article v-for="member in team" :key="member.name" class="team-member">
      <img :src="member.image" :alt="member.name" />

      <div class="team-text">
        <h3>{{ member.name }} – {{ member.role }}</h3>
        <p>{{ member.description }}</p>
      </div>
    </article>
  </section>
</template>

<style scoped>
.team-section {
  padding: 4rem;
  background-color: #fff5e6;
}

.team-section h2 {
  color: #b70064;
  margin-bottom: 3rem;
  width: 342;
  height: 46;
  top: 442px;
  left: 266px;
  opacity: 1;
  font-family: Jersey 10;
  font-weight: 400;
  font-style: Regular;
  font-size: 48px;
  line-height: 100%;
  letter-spacing: 0%;
}

.team-member {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
}

.team-member img {
  width: 123;
  height: 123;
  top: 506px;
  left: 256px;
  opacity: 1;
}

.team-text h3 {
  width: 699;
  height: 21;
  top: 518px;
  left: 399px;
  opacity: 1;
  font-family: Jersey 10;
  font-weight: 400;
  font-style: Regular;
  font-size: 20px;
  line-height: 100%;
  letter-spacing: 0%;
  text-align: justify;
  color: #000000;
}

.team-text p {
  font-family: Inter;
  font-weight: 300;
  font-style: Light;
  font-size: 13px;
  line-height: 100%;
  letter-spacing: 0%;
  text-align: justify;
  width: 632;
  height: 47;
  top: 544px;
  left: 399px;
  opacity: 1;
}
</style>
