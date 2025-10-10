db.createCollection("categories", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_categorie", "name_categorie"],
            properties: {
                id_categorie: {
                    bsonType: "string",
                    description: "identifiant unique de la catégorie"
                },
                nom_categorie: {
                    bsonType: "string",
                    description: "nom de la catégorie (ex: 'Vêtements', 'Accessoires')"
                }
            }
        }
    }
});