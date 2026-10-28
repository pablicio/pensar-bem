# Estágio 1: compilar e publicar, com o SDK
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS compilacao
WORKDIR /src

COPY global.json Prefeitura.slnx dotnet-tools.json ./
COPY Prefeitura.Dominio/*.csproj Prefeitura.Dominio/
COPY Prefeitura.Infraestrutura/*.csproj Prefeitura.Infraestrutura/
COPY Prefeitura.Api/*.csproj Prefeitura.Api/
RUN dotnet restore Prefeitura.Api/Prefeitura.Api.csproj

COPY Prefeitura.Dominio/ Prefeitura.Dominio/
COPY Prefeitura.Infraestrutura/ Prefeitura.Infraestrutura/
COPY Prefeitura.Api/ Prefeitura.Api/
RUN dotnet publish Prefeitura.Api/Prefeitura.Api.csproj \
    -c Release -o /publicado --no-restore

# Estágio 2: as migrations, num executável só
FROM compilacao AS bundle
RUN dotnet tool restore
RUN dotnet ef migrations bundle \
    --project Prefeitura.Infraestrutura \
    --startup-project Prefeitura.Api \
    --self-contained -r linux-x64 -o /efbundle

FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-noble-chiseled \
    AS migracoes
COPY --from=bundle /efbundle /efbundle
ENTRYPOINT ["/efbundle"]

# Estágio 3: só o necessário para rodar a API
FROM mcr.microsoft.com/dotnet/aspnet:10.0-noble-chiseled-extra
WORKDIR /app
COPY --from=compilacao /publicado .
ENTRYPOINT ["dotnet", "Prefeitura.Api.dll"]
