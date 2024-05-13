CREATE TABLE "password" (id INTEGER PRIMARY KEY, user_id INTEGER, service BLOB, login BLOB, password BLOB);
CREATE TABLE "user" (
	"id"	INTEGER,
	"login"	TEXT,
	"password"	TEXT,
	"secret"	TEXT,
	"created"	TEXT,
	"updated"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
