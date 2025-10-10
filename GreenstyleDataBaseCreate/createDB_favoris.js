db.createCollection("favorites", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["fav_id", "fav_name", "user_id", "cover_image", "site_list"],
            properties: {
                board_id: {
                    bsonType: "string",
                    description: "Identifiant unique du tableau de favoris"
                },
                board_name: {
                    bsonType: "string",
                    description: "Nom du tableau de favoris (ex: 'Mes marques éthiques')"
                },
                user_id: {
                    bsonType: "string",
                    description: "Clé étrangère vers l'ID de l'utilisateur"
                },
                cover_image: {
                    bsonType: "string",
                    description: "URL de l'image de couverture du tableau"
                },
                site_list: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    },
                    description: "Tableau de références aux identifiants des sites favoris"
                }
            }
        }
    }
});