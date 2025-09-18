/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'greenstyle_DB;';

// The current database to use.
use(database);

db.createCollection("brands", {
validator: {
    $jsonSchema: {
        bsonType: "object",
            required: ["id_marque", "nom_marque", "lien_web", "categorie_marque", "gamme_prix", "matieres_resp", "certifications", "pays_origine", "gestions_invendues", "transparence_chaines", "impact_env_global", "ethique_travail", "score_final", "description_marque", "sites_associes"],
                properties: {
            id_marque: {
                bsonType: "string",
                    description: "identifiant unique de la marque"
            },
            nom_marque: {
                bsonType: "string",
                    description: "nom de la marque"
            },
            logo: {
                bsonType: "string",
                    description: "URL du logo de la marque"
            },
            lien_web: {
                bsonType: "string",
                    description: "URL du site web de la marque"
            },
            categorie_marque: {
                bsonType: "string",
                    description: "catégorie de la marque (ex: 'vêtements', 'accessoires')"
            },
            gamme_prix: {
                bsonType: "int",
                    description: "gamme de prix de la marque (note sur 5)"
            },
            matieres_resp: {
                bsonType: "int",
                    description: "pourcentage de matières responsables"
            },
            certifications: {
                bsonType: "array",
                    description: "liste de certifications de la marque (ex: ['GOTS', 'Fair Trade'])"
            },
            pays_origine: {
                bsonType: "string",
                    description: "pays d'origine de la marque"
            },
            gestions_invendues: {
                bsonType: "string",
                    description: "politique de gestion des invendus"
            },
            transparence_chaines: {
                bsonType: "string",
                    description: "niveau de transparence de la chaîne d'approvisionnement"
            },
            impact_env_global: {
                bsonType: "double",
                    description: "score d'impact environnemental (note sur 5)"
            },
            ethique_travail: {
                bsonType: "double",
                    description: "score d'éthique du travail (note sur 5)"
            },
            score_final: {
                bsonType: "double",
                    description: "score final (moyenne des deux scores, sur 5)"
            },
            description_marque: {
                bsonType: "string",
                    description: "description de la marque"
            },
            sites_associes: {
                bsonType: "array",
                    items: {
                    bsonType: "string"
                },
                description: "tableau de références aux identifiants des sites de la marque"
            }
        }
    }
}
});

// More information on the `createCollection` command can be found at:
// https://www.mongodb.com/docs/manual/reference/method/db.createCollection/
