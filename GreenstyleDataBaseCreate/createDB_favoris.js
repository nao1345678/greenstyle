db.createCollection("favoris", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_tableau", "nom_tableau", "id_user", "image_couverture", "listes_sites"],
            properties: {
                id_tableau: {
                    bsonType: "string",
                    description: "identifiant unique du tableau de favoris"
                },
                nom_tableau: {
                    bsonType: "string",
                    description: "nom du tableau de favoris (ex: 'Mes marques éthiques')"
                },
                id_user: {
                    bsonType: "string",
                    description: "clé étrangère vers l'ID de l'utilisateur"
                },
                image_couverture: {
                    bsonType: "string",
                    description: "URL de l'image de couverture du tableau"
                },
                listes_sites: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    },
                    description: "tableau de références aux identifiants des sites favoris"
                }
            }
        }
    }
});

