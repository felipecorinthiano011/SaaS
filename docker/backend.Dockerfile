FROM maven:3.9.8-eclipse-temurin-21 AS build
WORKDIR /app

COPY backend/pom.xml backend/pom.xml
RUN mvn -f backend/pom.xml -q -DskipTests dependency:go-offline

COPY backend backend
RUN mvn -f backend/pom.xml -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /opt/app
COPY --from=build /app/backend/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]

