// Sélectionner / créer la base
use greenstyle_DB;

// ---------------- USERS ----------------
db.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_utilisateur", "nom_utilisateur", "prenom_utilisateur", "mail", "mot_de_passe"],
            properties: {
                id_utilisateur: { bsonType: "string", description: "ID unique de l'utilisateur" },
                nom_utilisateur: { bsonType: "string", description: "nom de l'utilisateur" },
                prenom_utilisateur: { bsonType: "string", description: "prénom de l'utilisateur" },
                mail: { bsonType: "string", description: "email unique de l'utilisateur" },
                mot_de_passe: { bsonType: "string", description: "mot de passe hashé" }
            }
        }
    }
});
db.users.createIndex({ "mail": 1 }, { unique: true });

// ---------------- CATEGORIES ----------------
db.createCollection("categories", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_categorie", "nom_categorie"],
            properties: {
                id_categorie: { bsonType: "string", description: "ID unique de la catégorie" },
                nom_categorie: { bsonType: "string", description: "nom de la catégorie" }
            }
        }
    }
});

// ---------------- BRANDS ----------------
db.createCollection("brands", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_marque", "nom_marque", "lien_web"],
            properties: {
                id_marque: { bsonType: "string", description: "ID unique de la marque" },
                nom_marque: { bsonType: "string", description: "nom de la marque" },
                logo: { bsonType: "string", description: "URL du logo" },
                lien_web: { bsonType: "string", description: "site web de la marque" },
                id_categorie: {
                    bsonType: "array",
                    items: { bsonType: "string" },
                    description: "liste des catégories associées"
                },
                gamme_prix: { bsonType: "int", description: "note prix (sur 5)" },
                matieres_resp: { bsonType: "int", description: "% matières responsables" },
                certifications: { bsonType: "array", items: { bsonType: "string" }, description: "certifications" },
                pays_origine: { bsonType: "string", description: "pays d'origine" },
                pays_production: { bsonType: "string", description: "pays de production" },
                gestions_invendues: { bsonType: "string", description: "gestion des invendus" },
                transparence_chaines: { bsonType: "string", description: "niveau transparence chaîne" },
                impact_env_global: { bsonType: "double", description: "note impact environnement (sur 5)" },
                ethique_travail: { bsonType: "double", description: "note éthique travail (sur 5)" },
                score_final: { bsonType: "double", description: "score final calculé" },
                description_marque: { bsonType: "string", description: "description" },
                badge_planete: { bsonType: "bool", description: "badge d'excellence planète" },
                badge_travail: { bsonType: "bool", description: "badge d'excellence travail" },
                sites_associes: { bsonType: "array", items: { bsonType: "string" }, description: "liste des sites" }
            }
        }
    }
});

// ---------------- ALTERNATIVES ----------------
db.createCollection("alternatives", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_alternative", "description", "id_marque", "categorie"],
            properties: {
                id_alternative: { bsonType: "string", description: "ID unique alternative" },
                description: { bsonType: "string", description: "description" },
                id_marque: { bsonType: "string", description: "clé étrangère vers la marque" },
                categorie: { bsonType: "string", description: "catégorie concernée" }
            }
        }
    }
});

// ---------------- SITES ----------------
db.createCollection("sites", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_site", "nom_site", "url"],
            properties: {
                id_site: { bsonType: "string", description: "ID unique site" },
                nom_site: { bsonType: "string", description: "nom du site" },
                url: { bsonType: "string", description: "url du site" }
            }
        }
    }
});

// ---------------- FAVORIS ----------------
db.createCollection("favoris", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_favori", "id_user", "id_marque"],
            properties: {
                id_favori: { bsonType: "string", description: "ID unique du favori" },
                id_user: { bsonType: "string", description: "clé étrangère utilisateur" },
                id_marque: { bsonType: "string", description: "clé étrangère marque" },
                listes_sites: { bsonType: "array", items: { bsonType: "string" }, description: "sites associés" }
            }
        }
    }
});
