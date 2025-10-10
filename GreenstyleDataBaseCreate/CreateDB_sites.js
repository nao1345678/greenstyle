/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'greenstyle_DB;';

// The current database to use.
use(database);

db.createCollection("sites", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["site_id", "site_name", "url"],
            properties: {
                site_id: {
                    bsonType: "string",
                    description: "Identifiant unique du site"
                },
                site_name: {
                    bsonType: "string",
                    description: "Nom du site"
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
