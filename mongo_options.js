db.createCollection("User", {validator:{$or: [ {name:{$exists:true},password:{$exists:true}} ] } } )
db.createCollection("UPC", {validator:{$or: [ {upc:{$exists:true}} ] } } )
db.User.createIndex( { "name": 1 }, { unique: true } )