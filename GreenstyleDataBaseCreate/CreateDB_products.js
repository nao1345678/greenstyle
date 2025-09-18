/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'greenstyle_DB;';

// The current database to use.
use(database);

// Create a new collection.
db.createCollection("products", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_produit", "nom_produit", "description_produit", "alternatives_inspirees"],
            properties: {
                id_produit: {
                    bsonType: "string",
                    description: "identifiant unique du produit"
                },
                nom_produit: {
                    bsonType: "string",
                    description: "nom du produit"
                },
                description_produit: {
                    bsonType: "string",
                    description: "description du produit"
                },
                alternatives_inspirees: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    },
                    description: "tableau de références aux identifiants des alternatives inspirées par ce produit"
                }
            }
        }
    }
});

// More information on the `createCollection` command can be found at:
// https://www.mongodb.com/docs/manual/reference/method/db.createCollection/
