/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'greenstyle_DB;';

// The current database to use.
use(database);

// Create a new collection.
db.createCollection("sites", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_site", "nom_site", "url"],
            properties: {
                id_site: {
                    bsonType: "string",
                    description: "identifiant unique du site"
                },
                nom_site: {
                    bsonType: "string",
                    description: "nom du site"
                },
                url: {
                    bsonType: "string",
                    description: "URL du site"
                }
            }
        }
    }
});

// More information on the `createCollection` command can be found at:
// https://www.mongodb.com/docs/manual/reference/method/db.createCollection/
