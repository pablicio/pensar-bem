FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /build
COPY pom.xml .
RUN --mount=type=cache,target=/root/.m2 \
    mvn -q dependency:go-offline
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 \
    mvn -q package -DskipTests

FROM eclipse-temurin:21-jre
RUN useradd --create-home --uid 10001 fiscal
WORKDIR /app
COPY --from=builder /build/target/fiscal.jar app.jar
USER fiscal
ENV TZ=America/Sao_Paulo \
    JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75"
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
