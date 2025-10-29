/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'greenstyle_DB;';

// The current database to use.
use(database);

db.createCollection("alternatives", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_alternative", "description", "id_marque", "proposé_pour_la_catégorie"],
            properties: {
                id_alternative: {
                    bsonType: "string",
                    description: "identifiant unique de l'alternative"
                },
                description: {
                    bsonType: "string",
                    description: "description de l'alternative"
                },
                id_marque: {
                    bsonType: "string",
                    description: "clé étrangère vers l'ID de la marque"
                },
                proposé_pour_la_catégorie: {
                    bsonType: "string",
                    description: "catégorie de produit pour laquelle l'alternative est proposée"
                }
            }
        }
    }
});