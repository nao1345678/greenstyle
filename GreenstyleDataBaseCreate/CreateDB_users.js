/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'greenstyle_DB;';

// The current database to use.
use(database);

db.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "last_name", "first_name", "email", "password"],
            properties: {
                user_id: {
                    bsonType: "string",
                    description: "Identifiant unique de l'utilisateur"
                },
                last_name: {
                    bsonType: "string",
                    description: "Nom de famille de l'utilisateur"
                },
                first_name: {
                    bsonType: "string",
                    description: "Prénom de l'utilisateur"
                },
                email: {
                    bsonType: "string",
                    description: "Adresse email de l'utilisateur"
                },
                password: {
                    bsonType: "string",
                    description: "Mot de passe hashé de l'utilisateur"
                }
            }
        }
    }
});
db.users.createIndex({ "email": 1 }, { unique: true });