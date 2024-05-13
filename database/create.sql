CREATE TABLE "user" (
	"id"	INTEGER,
	"login"	TEXT,
	"password"	TEXT,
	"secret"	TEXT,
	"created"	TEXT,
	"updated"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "password" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"service"	TEXT,
	"login"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE
);
