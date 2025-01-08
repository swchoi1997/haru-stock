// spring_chat 데이터베이스를 생성하고 기본 컬렉션을 만듭니다.
db = db.getSiblingDB('haru_stock');

// root 사용자 생성
db.createUser({
    user: 'root',
    pwd: 'root',
    roles: [
        { role: 'root', db: 'admin' }
    ]
});

// spring_chat 데이터베이스에 대한 사용자 생성 (필요한 경우)
db.createUser({
    user: 'haru',
    pwd: 'haru',
    roles: [{ role: 'readWrite', db: 'haru_stock' }]
});

// 기본 컬렉션에 문서 하나 삽입
db.example_collection.insertOne({ message: 'Hello, MongoDB!' });
