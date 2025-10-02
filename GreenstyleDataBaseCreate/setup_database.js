// Select / create the database
db = db.getSiblingDB('greenstyle_DB');

// ---------------- USERS ----------------
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["username", "firstname", "email", "password"],
      properties: {
        username: { bsonType: "string", description: "user login name" },
        firstname: { bsonType: "string", description: "first name" },
        email: { bsonType: "string", description: "unique user email" },
        password: { bsonType: "string", description: "bcrypt hashed password" }
      }
    }
  }
});
// unique email
db.users.createIndex({ email: 1 }, { unique: true });

// ---------------- CATEGORIES ----------------
db.createCollection("categories", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name"],
      properties: {
        name: { bsonType: "string", description: "category name" }
      }
    }
  }
});

// ---------------- BRANDS ----------------
db.createCollection("brands", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["brand_name"],
      properties: {
        brand_name: { bsonType: "string", description: "brand name" },
        logo: { bsonType: "string", description: "logo URL" },
        website: { bsonType: "string", description: "brand website" },
        category_id: { bsonType: ["string", "null"], description: "single category id (optional)" },

        price_range: { bsonType: ["double", "int", "null"], description: "price score (0–5)" },
        sustainable_materials: { bsonType: ["double", "int", "null"], description: "responsible materials % / score" },
        certifications: { bsonType: ["string", "null"], description: "certifications (free text or CSV)" },
        country_origin: { bsonType: ["string", "null"], description: "origin country" },
        country_production: { bsonType: ["string", "null"], description: "production country" },
        unsold_management: { bsonType: ["string", "null"], description: "unsold stock policy" },
        supply_chain_transparency: { bsonType: ["string", "null"], description: "transparency level" },

        global_env_impact: { bsonType: ["double", "int", "null"], description: "environment impact score (0–5)" },
        labor_ethics: { bsonType: ["double", "int", "null"], description: "labor ethics score (0–5)" },
        final_score: { bsonType: ["double", "int", "null"], description: "final score (0–5)" },

        short_description: { bsonType: ["string", "null"], description: "short description" },
        description: { bsonType: ["string", "null"], description: "long description" },

        planet_badge: { bsonType: ["bool", "null"], description: "planet excellence badge" },
        labor_badge: { bsonType: ["bool", "null"], description: "labor excellence badge" },

        // if you later want to link sites by id strings:
        site_ids: {
          bsonType: ["array", "null"],
          items: { bsonType: "string" },
          description: "related site ids (optional)"
        }
      }
    }
  }
});
// helpful indexes
db.brands.createIndex({ brand_name: 1 });

// ---------------- ALTERNATIVES ----------------
db.createCollection("alternatives", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["description"],
      properties: {
        description: { bsonType: "string", description: "alternative description" },
        brand_id: { bsonType: ["string", "null"], description: "FK to brands._id as string (optional)" },
        category: { bsonType: ["string", "null"], description: "target category (optional)" }
      }
    }
  }
});

// ---------------- SITES ----------------
db.createCollection("sites", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["url"],
      properties: {
        url: { bsonType: "string", description: "site URL" },
        // optional: keep links to brand ids as strings if you need
        brand_ids: {
          bsonType: ["array", "null"],
          items: { bsonType: "string" },
          description: "related brand ids (optional)"
        }
      }
    }
  }
});
// helpful indexes
db.sites.createIndex({ url: 1 }, { unique: true });

// ---------------- FAVORITES ----------------
db.createCollection("favorites", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "brand_id"],
      properties: {
        user_id: { bsonType: "string", description: "FK to users._id as string" },
        brand_id: { bsonType: "string", description: "FK to brands._id as string" },
        site_ids: {
          bsonType: ["array", "null"],
          items: { bsonType: "string" },
          description: "optional related site ids"
        }
      }
    }
  }
});
