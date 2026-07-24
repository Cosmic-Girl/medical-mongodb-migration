db = db.getSiblingDB("medical_db");

db.createUser({
  user: "migration_user",
  pwd: "mot_de_passe_migration",
  roles: [
    {
      role: "readWrite",
      db: "medical_db"
    }
  ]
});

db.createUser({
  user: "medical_reader",
  pwd: "mot_de_passe_lecture",
  roles: [
    {
      role: "read",
      db: "medical_db"
    }
  ]
});