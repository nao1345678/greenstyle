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
            required: ["brand_id", "brand_name", "web_link", "brand_category", "price_range", "responsible_materials", "certifications", "country_of_origin", "unsold_management", "supply_chain_transparency", "global_environmental_impact", "labor_ethics", "final_score", "brand_description", "associated_sites"],
            properties: {
                brand_id: {
                    bsonType: "string",
                    description: "Identifiant unique de la marque"
                },
                brand_name: {
                    bsonType: "string",
                    description: "Nom de la marque"
                },
                logo: {
                    bsonType: "string",
                    description: "URL du logo de la marque"
                },
                web_link: {
                    bsonType: "string",
                    description: "URL du site web de la marque"
                },
                brand_category: {
                    bsonType: "string",
                    description: "Catégorie de la marque (ex: 'vêtements', 'accessoires')"
                },
                price_range: {
                    bsonType: "int",
                    description: "Gamme de prix de la marque (note sur 5)"
                },
                responsible_materials: {
                    bsonType: "int",
                    description: "Pourcentage de matières responsables"
                },
                certifications: {
                    bsonType: "array",
                    description: "Liste des certifications de la marque (ex: ['GOTS', 'Fair Trade'])"
                },
                country_of_origin: {
                    bsonType: "string",
                    description: "Pays d'origine de la marque"
                },
                country_of_production: {
                    bsonType: "array",
                    description: "Pays de production de la marque"
                },
                unsold_management: {
                    bsonType: "string",
                    description: "Politique de gestion des invendus"
                },
                supply_chain_transparency: {
                    bsonType: "string",
                    description: "Niveau de transparence de la chaîne d'approvisionnement"
                },
                global_environmental_impact: {
                    bsonType: "double",
                    description: "Score d'impact environnemental (note sur 5)"
                },
                labor_ethics: {
                    bsonType: "double",
                    description: "Score d'éthique du travail (note sur 5)"
                },
                final_score: {
                    bsonType: "double",
                    description: "Score final (moyenne des deux scores, sur 5)"
                },
                brand_description: {
                    bsonType: "string",
                    description: "Description de la marque"
                },
                associated_sites: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    },
                    description: "Tableau de références aux identifiants des sites associés à la marque"
                }
            }
        }
    }
});
// More information on the `createCollection` command can be found at:
// https://www.mongodb.com/docs/manual/reference/method/db.createCollection/
