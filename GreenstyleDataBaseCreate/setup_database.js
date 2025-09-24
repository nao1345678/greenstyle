
// Se connecter à la base de données 'greenstyle_DB'.
// Si la base n'existe pas, MongoDB s'en charge automatiquement 
use greenstyle_DB;

// Créer la collection 'users'
// decription afin decrir que fait une colonne 
db.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_utilisateur", "nom_utilisateur", "prénom_utilisateur", "mail", "mot_de_passe"],
            properties: {
                id_utilisateur: {
                    bsonType: "string",
                    description: "identifiant unique de l'utilisateur"
                },
                nom_utilisateur: {
                    bsonType: "string",
                    description: "nom de famille de l'utilisateur"
                },
                prénom_utilisateur: {
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


// Créer la collection 'brands'
db.createCollection("brands", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_marque", "nom_marque", "lien_web", "categorie_marque", "gamme_prix", "matieres_resp", "certifications", "pays_origine", "gestions_invendues", "transparence_chaines", "impact_env_global", "ethique_travail", "score_final", "description_marque", "sites_associes"],
            properties: {
                id_marque: {
                    bsonType: "string",
                    description: "identifiant unique de la marque"
                },
                nom_marque: {
                    bsonType: "string",
                    description: "nom de la marque"
                },
                logo: {
                    bsonType: "string",
                    description: "URL du logo de la marque"
                },
                lien_web: {
                    bsonType: "string",
                    description: "URL du site web de la marque"
                },
                id_categorie: {
                    bsonType: "int",
                    description: "clé étrangère vers l'ID de la marque"
                },
                gamme_prix: {
                    bsonType: "int",
                    description: "gamme de prix de la marque (note sur 5)"
                },
                matieres_resp: {
                    bsonType: "int",
                    description: "pourcentage de matières responsables"
                },
                certifications: {
                    bsonType: "array",
                    description: "liste de certifications de la marque (ex: ['GOTS', 'Fair Trade'])"
                },
                pays_origine: {
                    bsonType: "string",
                    description: "pays d'origine de la marque"
                },
                gestions_invendues: {
                    bsonType: "string",
                    description: "politique de gestion des invendus"
                },
                transparence_chaines: {
                    bsonType: "string",
                    description: "niveau de transparence de la chaîne d'approvisionnement"
                },
                impact_env_global: {
                    bsonType: "double",
                    description: "score d'impact environnemental (note sur 5)"
                },
                ethique_travail: {
                    bsonType: "double",
                    description: "score d'éthique du travail (note sur 5)"
                },
                score_final: {
                    bsonType: "double",
                    description: "score final (moyenne des deux scores, sur 5)"
                },
                description_marque: {
                    bsonType: "string",
                    description: "description de la marque"
                },
                sites_associes: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    },
                    description: "tableau de références aux identifiants des sites de la marque"
                }
            }
        }
    }
});

// Créer la collection 'alternatives'
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

// Créer la collection 'sites'
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

// Créer la collection 'favoris'
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

// Créer la collection 'categories'
db.createCollection("categories", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["id_categorie", "nom_categorie"],
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
