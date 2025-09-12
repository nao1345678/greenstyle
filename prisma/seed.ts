import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // Création d'un utilisateur
  const utilisateur = await prisma.utilisateur.create({
    data: {
      nom_utilisateur: "dupont",
      prénom: "Alice",
      mail: "alice.dupont@example.com",
      mot_de_passe: "hashedpassword123", // 🔒 à hasher en vrai projet
    },
  });

  // Création d'une marque
  const marque = await prisma.marque.create({
    data: {
      nom_marque: "Zara",
      logo: "https://example.com/logo.png",
      lien_web: "https://zara.com",
      catégorie_marque: "fast fashion",
      gamme_prix: "bas",
      matières_resp: "peu",
      certifications: "aucune",
      pays_origine: "Espagne",
      gestions_invendues: false,
      transparence_chaînes: "faible",
      impact_env_global: 40,
      éthique_travail: "controversée",
      score_final: 42,
      description_marque: "Marque de fast fashion mondiale",
      utilisateurs: {
        connect: { id: utilisateur.id },
      },
    },
  });

  // Ajout d'une alternative
  const alternative = await prisma.alternative.create({
    data: {
      description: "Production locale et durable",
      marque: { connect: { id: marque.id } },
    },
  });

  // Ajout d’un produit inspiré par l’alternative
  const produit = await prisma.produit.create({
    data: {
      nom_produit: "T-shirt bio",
      description_produit: "Fabriqué en coton bio certifié",
      alternative: { connect: { id: alternative.id } },
    },
  });

  // Ajout d’un site officiel pour la marque
  const site = await prisma.site.create({
    data: {
      nom_site: "Zara France",
      url: "https://zara.com/fr",
      marques: {
        connect: { id: marque.id },
      },
    },
  });

  console.log("✅ Seed terminé avec succès !");
  console.log({ utilisateur, marque, alternative, produit, site });
}

main()
  .catch((e) => {
    console.error("Erreur lors du seed :", e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
