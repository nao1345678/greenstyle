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
            required: ["id_utilisateur", "nom_utilisateur", "prénom", "mail", "mot_de_passe"],
            properties: {
                id_utilisateur: {
                    bsonType: "string",
                    description: "identifiant unique de l'utilisateur"
                },
                nom_utilisateur: {
                    bsonType: "string",
                    description: "nom de famille de l'utilisateur"
                },
                prénom: {
                    bsonType: "string",
                    description: "prénom de l'utilisateur"
                },
                mail: {
                    bsonType: "string",
                    description: "adresse email de l'utilisateur"
                },
                mot_de_passe: {
                    bsonType: "string",
                    description: "mot de passe hashé de l'utilisateur"
                }
            }
        }
    }
});
db.users.createIndex({ "mail": 1 }, { unique: true });